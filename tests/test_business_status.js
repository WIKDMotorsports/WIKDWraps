
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

function formatTime(hourFloat) {
    if (hourFloat === null) return 'Closed';
    const hours = Math.floor(hourFloat);
    const minutes = Math.round((hourFloat - hours) * 60);
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const displayHours = hours % 12 || 12;
    const displayMinutes = minutes < 10 ? '0' + minutes : minutes;
    return `${displayHours}:${displayMinutes} ${ampm}`;
}

// Logic extracted from index.html for testing purposes
// In a real build system, we might export this from a module.
// Here we duplicate the logic to verify its correctness.
function getBusinessStatusFixed(hours) {
    const now = new Date();
    const BUSINESS_TIMEZONE = 'America/Chicago';

    // Convert current time to 'America/Chicago' (Central Time)
    // We use hour12: false to get 0-23 hours easily
    const formatter = new Intl.DateTimeFormat('en-US', {
        timeZone: BUSINESS_TIMEZONE,
        weekday: 'short',
        hour: 'numeric',
        minute: 'numeric',
        hour12: false
    });

    const parts = formatter.formatToParts(now);
    const partMap = {};
    parts.forEach(p => partMap[p.type] = p.value);

    // partMap['weekday'] returns "Sun", "Mon", etc. matching DAYS
    const dayStr = partMap['weekday'];
    const dayIndex = DAYS.indexOf(dayStr);

    if (dayIndex === -1) {
        console.error(`Invalid day string received from Intl: ${dayStr}`);
        return { isOpen: false, statusText: 'ERROR' };
    }

    const hour = parseInt(partMap['hour'], 10);
    const minute = parseInt(partMap['minute'], 10);

    const currentDay = DAYS[dayIndex];
    // Calculate float hour (e.g., 8:30 -> 8.5)
    const currentHourFloat = hour + minute / 60;

    const todayHours = hours[currentDay];

    // Check if open now
    const isOpen = todayHours.open !== null &&
                   currentHourFloat >= todayHours.open &&
                   currentHourFloat < todayHours.close;

    if (isOpen) {
        return { isOpen: true, statusText: 'OPEN' };
    }

    // Look for next open time
    for (let i = 0; i < 7; i++) {
        const checkDayIndex = (dayIndex + i) % 7;
        const checkDay = DAYS[checkDayIndex];
        const dayHoursData = hours[checkDay];

        if (dayHoursData.open !== null) {
            if (i === 0) {
                // If checking today (and we know we are closed now),
                // we are only interested if it opens LATER today.
                if (currentHourFloat < dayHoursData.open) {
                    return { isOpen: false, nextOpenTime: formatTime(dayHoursData.open), nextOpenDay: 'TODAY' };
                }
            } else {
                // Future day
                return { isOpen: false, nextOpenTime: formatTime(dayHoursData.open), nextOpenDay: checkDay.toUpperCase() };
            }
        }
    }

    return { isOpen: false, statusText: 'CLOSED FOR WEEK' };
}

// Test Configuration
const pbwHours = { 'Sun': { open: null, close: null, closedText: 'Closed' }, 'Mon': { open: 8.5, close: 17 }, 'Tue': { open: 8.5, close: 17 }, 'Wed': { open: 8.5, close: 17 }, 'Thu': { open: 8.5, close: 17 }, 'Fri': { open: 8.5, close: 17 }, 'Sat': { open: null, close: null, closedText: 'Closed' } };

// Mock Date to control time
const originalDate = Date;

function runTest(utcTimeStr, expectedIsOpen, description) {
    global.Date = class extends Date {
        constructor(date) {
            if (date) return new originalDate(date);
            return new originalDate(utcTimeStr);
        }
    };

    // Ensure Intl uses the mocked date properly?
    // Intl.DateTimeFormat uses the Date object passed to formatToParts.
    // So passing `new Date()` (which is mocked) should work.

    const status = getBusinessStatusFixed(pbwHours);
    console.log(`Test: ${description}`);
    console.log(`Time (UTC): ${utcTimeStr}`);
    console.log(`Result: ${status.isOpen ? 'OPEN' : 'CLOSED'} (${status.statusText || status.nextOpenTime})`);

    if (status.isOpen === expectedIsOpen) {
        console.log("PASS\n");
    } else {
        console.log(`FAIL. Expected ${expectedIsOpen}, got ${status.isOpen}\n`);
        process.exit(1);
    }
}

console.log("Running Business Status Tests...\n");

// Case 1: Monday 13:00 UTC (8:00 AM CST) -> Closed (Opens at 8:30)
runTest('2023-10-23T13:00:00Z', false, "Monday 8:00 AM CST (Before Open)");

// Case 2: Monday 14:00 UTC (9:00 AM CST) -> Open
runTest('2023-10-23T14:00:00Z', true, "Monday 9:00 AM CST (During Open)");

// Case 3: Monday 23:30 UTC (18:30 CST) -> Closed (Closes at 17:00 CST)
runTest('2023-10-23T23:30:00Z', false, "Monday 6:30 PM CST (After Close)");

// Case 4: Sunday 18:00 UTC (13:00 CST) -> Closed (Closed all day)
runTest('2023-10-22T18:00:00Z', false, "Sunday (Closed Day)");

console.log("All tests passed!");
