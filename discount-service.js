const promotions = [
  {
    code: 'WEEKLY10',
    description: '10% off rentals of 7 days or more',
    type: 'duration',
    minDays: 7,
    percentage: 10,
  },
  {
    code: 'WEEKEND5',
    description: '5% off 2-3 day weekend rentals',
    type: 'duration',
    minDays: 2,
    maxDays: 3,
    percentage: 5,
  },
  {
    code: 'FIRST15',
    description: '15% off first-time renters',
    type: 'customer',
    requiredStatus: 'new',
    percentage: 15,
  },
  {
    code: 'LOYAL10',
    description: '10% loyalty discount for returning customers',
    type: 'customer',
    requiredStatus: 'returning',
    percentage: 10,
  },
];

/**
 * Normalize a promo code to uppercase and trim whitespace.
 */
function normalizeCode(code) {
  return (code || '').toString().trim().toUpperCase();
}

function findPromotion(code) {
  return promotions.find((promo) => promo.code === normalizeCode(code));
}

function calculateDurationDiscount(baseRate, days, promo) {
  if (!promo) return 0;
  if (promo.type !== 'duration') return 0;
  if (days < promo.minDays) return 0;
  if (promo.maxDays && days > promo.maxDays) return 0;
  return Math.round((baseRate * days * promo.percentage) / 100);
}

function calculateCustomerDiscount(baseRate, days, customer, promo) {
  if (!promo) return 0;
  if (promo.type !== 'customer') return 0;
  if (!customer || !customer.status) return 0;
  if (normalizeCode(customer.status) !== normalizeCode(promo.requiredStatus)) return 0;
  return Math.round((baseRate * days * promo.percentage) / 100);
}

function calculateBaseTotal(baseRate, days) {
  return Math.round(baseRate * days);
}

function calculateDiscounts(options = {}) {
  const { baseRate = 0, days = 0, promoCode = '', customer = {} } = options;
  const promo = findPromotion(promoCode);
  const baseTotal = calculateBaseTotal(baseRate, days);
  let discountAmount = 0;
  let appliedPromotion = null;

  if (promo) {
    if (promo.type === 'duration') {
      discountAmount = calculateDurationDiscount(baseRate, days, promo);
      appliedPromotion = discountAmount > 0 ? promo : null;
    } else if (promo.type === 'customer') {
      discountAmount = calculateCustomerDiscount(baseRate, days, customer, promo);
      appliedPromotion = discountAmount > 0 ? promo : null;
    }
  }

  const total = Math.max(baseTotal - discountAmount, 0);

  return {
    baseRate,
    days,
    customer,
    promoCode: normalizeCode(promoCode),
    appliedPromotion,
    discountAmount,
    baseTotal,
    total,
  };
}

function getAvailablePromotions() {
  return promotions.map(({ code, description, type, percentage, minDays, maxDays, requiredStatus }) => ({
    code,
    description,
    type,
    percentage,
    minDays,
    maxDays,
    requiredStatus,
  }));
}

function describeBooking(booking) {
  const { baseRate = 0, days = 0, customer = {}, promoCode = '' } = booking;
  const result = calculateDiscounts({ baseRate, days, promoCode, customer });

  return {
    summary: `Booking for ${days} day(s) at $${baseRate.toFixed(2)}/day`,
    discount: result.discountAmount,
    total: result.total,
    appliedPromotion: result.appliedPromotion?.code || null,
    details: result,
  };
}

module.exports = {
  getAvailablePromotions,
  calculateDiscounts,
  describeBooking,
  findPromotion,
};
