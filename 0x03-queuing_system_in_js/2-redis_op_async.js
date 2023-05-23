import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('connect', () => console.log('Redis client connected to the server'));

client.on('error', err => console.log('Redis client not connected to the server:', err.message));


function setNewSchool(schoolName, value) {
  client.set(schoolName, value, print);
}

async function displaySchoolValue(schoolName) {
  try {
    const getData = promisify(client.get).bind(client);
    const data = await getData(schoolName);
    console.log(data)
  } catch (error) {
    console.error(error);
  }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');