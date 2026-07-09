console.log("Assignment 2");
// Task 1
function func1(name) {

    // Create Map for each character
    const characters = new Map();
    characters.set("悟空", [0, 0, 2]);
    characters.set("辛巴", [-3, 3, 2]);
    characters.set("丁滿", [-1, 4, 0]);
    characters.set("貝吉塔", [-4, -1, 2]);
    characters.set("特南克斯", [1, -2, 2]);
    characters.set("弗利沙", [4, -1, 0]);

    if (!characters.has(name)) {
        console.log("Character " + name + " not found.");
        return;
    }

    let closest = [];
    let farthest = [];
    let minDiff = 0, maxDiff = 0;
    let distance = 0;

    characters.forEach((pos, char) => {
        if (char != name) {
            // Calculate distance between character and name
            distance = (Math.abs(characters.get(name)[0] - pos[0]) +
                        Math.abs(characters.get(name)[1] - pos[1]) + 
                          Math.abs(characters.get(name)[2] - pos[2]));
            
            // Update maxDiff if applicable
            if (distance > maxDiff) {
                farthest = [char];
                maxDiff = distance;
            } else if (distance == maxDiff) {
                farthest.push(char);
            }

            // Update minDiff if applicable
            if (distance < minDiff) {
                closest = [char];
                minDiff = distance;
            } else if (distance == minDiff || minDiff == 0) {
                closest.push(char);
                minDiff = distance;
            }
        }
    });
    console.log("最遠" + farthest.join("、") + "；最近" + closest.join("、"));
} 

func1("辛巴"); // print 最遠弗利沙；最近丁滿、貝吉塔 
func1("悟空"); // print 最遠丁滿、弗利沙；最近特南克斯 
func1("弗利沙"); // print 最遠辛巴，最近特南克斯 
func1("特南克斯"); // print 最遠丁滿，最近悟空
console.log("");



// Task 2
const booking = new Map();  // Available timeslots for each service

/**
 * Helper for parsing criteria value. 
 * 
 * @param {string} attr - The criteria being parsed {"c", "r", "name"}
 * @param {string} value - The criteria string
 * @returns {string|number} The parsed name of the criteria or the parsed numeric value of the criteria
 */
function parseHelper(attr, value) {
    if (value[0] == "=") {
        if (booking.has(value.slice(1))) {
            return value.slice(1);
        }

        if (attr == "c") {
            return parseInt(value.slice(1));
        } else {
            return parseFloat(value.slice(1));
        }
    } else {
        if (attr == "c") {
            return parseInt(value.slice(2));
        } else {
            return parseFloat(value.slice(2));
        }
    }
}


/** 
 * Helper for checking if the requested timeslot is available for the given service.
 * 
 * @param {string} serviceName - The name of the service
 * @param {number} start - Start hour 
 * @param {number} end - End hour
 * @returns {boolean} True if the timeslot is free; False if it is already booked
*/
function timeslotIsFree(serviceName, start, end) {
    // console.log(booking.get(service));
    if (end - start > 1) {
        for(let i = start+1; i < end; i++) {
            if (booking.get(serviceName)[i] == 1) {
                return false;
            }
        }
    } else {
        if (booking.get(serviceName)[start] == 1 &&
             booking.get(serviceName)[end] == 1) {
                return false;
             }
    }
    return true;
}


/**
 * Helper for updating the booking timeslot of a given service.
 * 
 * @param {string} serviceName - The name of the service to update 
 * @param {number} start - The start time of the booking
 * @param {number} end - The end time of the booking
 */
function updateBooking(serviceName, start, end) {
    for (let i=start; i <= end; i++) {
        booking.get(serviceName)[i] = 1;
    }
}


function func2(ss, start, end, criteria) { 
    // Exit early if no services are available
    if (ss.length == 0) {
        console.log("No services available.")
        return;
    }

    // Exit early if the requested time range is invalid
    if (end - start <= 0 || start > 24 || end < 0) {
        console.log("Invalid time range requested.");
        return;
    }

    // Create empty timeslots for each service throughout the day: available = 0; taken = 1
    if (booking.size == 0) {
        ss.forEach((service) => {
            booking.set(service.name, new Array(24).fill(0));
        })
    }

    // Begin main logic
    let closest = "";   // The current best matching service
    let minDiff = Infinity;  // Difference between criteria and the service
    let value = "";
    if (criteria[0] == "c") {
        // Parse criteria value
        value = parseHelper(criteria[0], criteria.slice(1));
        if (isNaN(value)) {
            console.log("Invalid criteria " + criteria);
            return;
        }

        // Find the best-matching sevice
        ss.forEach((service) => {
            if (criteria.slice(1, 3) == ">=") {
                if (service.c >= value) {
                    if ((service.c - value) < minDiff) {
                        if (timeslotIsFree(service.name, start, end)) {
                            closest = service.name;
                            minDiff = service.c - value;
                        }
                    }
                }
            } else {
                if (service.c <= value) {
                    if (closest == "") {
                        closest = service.name;
                    }
                    if (value - (service.c) < minDiff) { 
                        if (timeslotIsFree(service.name, start, end)) {
                            closest = service.name;
                            minDiff = value - service.c;
                        }
                    }
                }
            }
        })

        // Output the result
        if (closest == "") {
            console.log("Sorry");
        } else {
            updateBooking(closest, start, end);
            console.log(closest);
        }

    } else if (criteria[0] == "r") {
        // Parse criteria value
        value = parseHelper(criteria[0], criteria.slice(1));
        if (isNaN(value)) {
            console.log("Invalid criteria " + criteria);
            return;
        }

        // Find the best matching sevice
        ss.forEach((service) => {
            if (criteria.slice(1, 3) == ">=") {
                if (service.r >= value) {
                    if ((service.r - value) < minDiff) {
                        if (timeslotIsFree(service.name, start, end)) {
                            closest = service.name;
                            minDiff = service.r - value;
                        }
                    }
                }
            } else {
                if (service.r <= value) {
                    if (closest == "") {
                        closest = service.name;
                    }

                    if (value - service.r < minDiff) {
                        if (timeslotIsFree(service.name, start, end)) {
                            closest = service.name;
                            minDiff = value - service.r;
                        }
                    }
                }
            }
        })

        // Output the result
        if (closest == "") {
            console.log("Sorry");
        } else {
            updateBooking(closest, start, end);
            console.log(closest);
        }

    } else if (criteria.slice(0, 4) == "name") {
        // Parse criteria value
        value = parseHelper(criteria.slice(0, 4), criteria.slice(4));
        if (!booking.has(value)) {
            console.log("Service " + criteria.slice(5) + " not found.");
            return;
        }

        // Check timeslot availability
        if (timeslotIsFree(value, start, end)) {
            updateBooking(value, start, end);
            console.log(value);
        } else {
            console.log("Sorry");
            return;
        }

    } else {
        console.log("Invalid criteria" + criteria);
    }
}

const services=[ 
    {"name":"S1", "r":4.5, "c":1000}, 
    {"name":"S2", "r":3, "c":1200}, 
    {"name":"S3", "r":3.8, "c":800} 
]; 

func2(services, 15, 17, "c>=800"); // S3 
func2(services, 11, 13, "r<=4"); // S3 
func2(services, 10, 12, "name=S3"); // Sorry 
func2(services, 15, 18, "r>=4.5"); // S1 
func2(services, 16, 18, "r>=4"); // Sorry 
func2(services, 13, 17, "name=S1"); // Sorry 
func2(services, 8, 9, "c<=1500"); // S2
func2(services, 8, 9, "c<=1500"); // S1
console.log("");



// Task 3
function func3(index) { 
    let num = 25;
    for (let i=0; i < index; i++) {
        if (i % 4 == 0) {
            num -= 2;
        } else if (i % 4 == 1) {
            num -= 3;
        } else if (i % 4 == 2) {
            num += 1;
        } else {
            num += 2;
        }
    }
    console.log(num);
}

func3(1); // print 23 
func3(5); // print 21 
func3(10); // print 16 
func3(30); // print 6
console.log("");



// Task 4
function func4(sp, stat, n) { 
    let car = -1;
    let vacancy = Infinity;
    let overflow = Infinity;

    for (let i=0; i < stat.length; i++) {
        // Check for avaiable cars
        if (parseInt(stat[i]) == 0) {
            if (sp[i] == n) {
                console.log(i);
                return;
            } else if (sp[i] > n) {
                if ((sp[i] - n) < vacancy) {
                    car = i;
                    vacancy = sp[i] - n;
                }
            } else if (sp[i] < n && vacancy == Infinity) {
                if ((n - sp[i]) < overflow) {
                    car = i;
                    overflow = n - sp[i];
                }
            }
        }
    }
    console.log(car)
}

func4([3, 1, 5, 4, 3, 2], "101000", 2); // print 5 
func4([1, 0, 5, 1, 3], "10100", 4); // print 4 
func4([4, 6, 5, 8], "1000", 4); // print 2