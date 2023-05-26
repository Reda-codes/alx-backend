const express = require('express')
const redis = require('redis');
const { promisify } = require('util');

const listProducts = [
    {
        id: 1,
        name: 'Suitcase 250',
        price: 50,
        stock: 4
    },
    {
        id: 2,
        name: 'Suitcase 450',
        price: 100,
        stock: 10
    },
    {
        id: 3,
        name: 'Suitcase 650',
        price: 350,
        stock: 2
    },
    {
        id: 4,
        name: 'Suitcase 1050',
        price: 550,
        stock: 5
    }
]

const getItemById = (id) => {
    return listProducts.find((el) => el.id == id);
}

const app = express()
const port = 1245

const client = redis.createClient();

const reserveStockById = async (itemId, stock) => {
    const setData = promisify(client.set).bind(client);
    await setData(`item.${itemId}`, stock)
}

const getCurrentReservedStockById = async (itemId) => {
  const getData = promisify(client.get).bind(client);
  const data = await getData(`item.${itemId}`)
  return Number(data);
}

app.get('/list_products', (_req, res) => {
  res.json(listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock
  })));
});

app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(Number(itemId));
  if (!item) {
    return res.json({ status: 'Product not found' });
  }
  const reservedStock = await getCurrentReservedStockById(Number(itemId));
  const currentQuantity = item.stock - reservedStock;
  res.json({
    itemId: item.id,
    itemName: item.name,
    price: item.price,
    initialAvailableQuantity: item.stock,
    currentQuantity: currentQuantity,
  }
);

})

app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(Number(itemId));
  if (!item) {
    return res.json({ status: 'Product not found' });
  }
  const reservedStock = await getCurrentReservedStockById(Number(itemId));
  const availableStock = item.stock - reservedStock;
  if (availableStock < 1) {
    return res.json({ status: 'Not enough stock available', itemId: item.id });
  }
  await reserveStockById(Number(itemId), reservedStock + 1);
  res.json({ status: 'Reservation confirmed', itemId: item.id });
});

app.listen(port, () => {
  console.log(`app listening on port ${port}`)
})