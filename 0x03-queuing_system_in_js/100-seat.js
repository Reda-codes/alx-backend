const express = require('express')
const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');

const client = redis.createClient();

const reserveSeat = async (number) => {
  await promisify(client.set).bind(client)('available_seats', number);
}

reserveSeat(50);

const getCurrentAvailableSeats = async () => {
  const data = await promisify(client.get).bind(client)('available_seats');
  return Number(data);
}

let reservationEnabled = true;

const queue = kue.createQueue();

const app = express();
const port = 1245;

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue
    .create('reserve_seat')
    .save((err) => {
      if (err) {
        res.json({ status: 'Reservation failed' });
      } else {
        res.json({ status: 'Reservation in process' });
      }
    });

  job.on('complete', (_result) => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', async (_req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (_job, done) => {
    const seats = await getCurrentAvailableSeats();

    if (seats >= 1) {
      await reserveSeat(seats - 1);
      if (seats - 1 === 0) {
        reservationEnabled = false;
      }
      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});


app.listen(port, () => {
  console.log(`app listening on port ${port}`)
})