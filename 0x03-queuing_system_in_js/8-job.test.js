import kue from 'kue';
const { expect } = require('chai');

import createPushNotificationsJobs from './8-job.js';

const list1 = [
    {
        phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
    }
];

const list2 = {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
}

describe(' createPushNotificationsJobs', () => {

  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('Throws an error message', () => {
    expect(function(){
        createPushNotificationsJobs(list2, queue);
    }).to.throw('Jobs is not an array');
  });

  it('Create a new Job', () => {
    createPushNotificationsJobs(list1, queue);
    expect(queue.testMode.jobs.length).to.equal(list1.length);
    for (let i = 0; i < list1.length; i++) {
      const job = queue.testMode.jobs[i];
      expect(job.type).to.equal('push_notification_code_3');
      expect(job.data.phoneNumber).to.equal(list1[i].phoneNumber);
      expect(job.data.message).to.equal(list1[i].message);
    }
  });
});
