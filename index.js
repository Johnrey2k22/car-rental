const { describeBooking, getAvailablePromotions } = require('./discount-service');

const exampleBooking = describeBooking({
  baseRate: 60,
  days: 3,
  promoCode: 'WEEKEND5',
  customer: { status: 'new' },
});

console.log('Available promotions:');
console.table(getAvailablePromotions());
console.log('\nExample booking output:');
console.log(JSON.stringify(exampleBooking, null, 2));
