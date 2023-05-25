import kue from 'kue';

const queue = kue.createQueue();

const jobData = {
  phoneNumber: '4153518780',
  message: 'This is the code to verify your account',
}

const job = queue.create('push_notification_code', jobData)
  .save((err) => {
    if (err) {
      console.error(err);
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  });

queue.on('complete', () => {
  console.log('Notification job completed');
});

queue.on('failed', () => {
  console.log('Notification job failed');
});