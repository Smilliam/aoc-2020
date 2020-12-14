use std::env;
use std::fs;
use std::io::{self, BufRead};

fn main() {
    let args: Vec<String> = env::args().collect();

    let filename = &args[1];
    let file = fs::File::open(filename).expect("Unable to open file");
    let mut reader = io::BufReader::new(file);

    let mut buf = String::new();
    reader.read_line(&mut buf).expect("failed to read line");
    let timestamp: u64 = buf.trim().parse().unwrap();
    println!("{}", timestamp);

    buf.clear();
    reader.read_line(&mut buf).expect("failed to read line");
    let buses: String = buf.trim().to_string();

    println!("{}", buses);

    let mut bus_nums: Vec<u64> = Vec::new();
    for split in buses.split(",") {
        if split != "x" {
            bus_nums.push(split.parse().unwrap());
            println!("{}", split);
        }
    }

    let mut min_bus: u64 = u64::MAX;
    let mut min_time: u64 = u64::MAX;
    for bus in bus_nums {
        let mut time: u64 = timestamp;
        while time % bus != 0 {
            time += 1;
        }

        let time_after: u64 = time - timestamp;
        if time_after < min_time {
            min_time = time_after;
            min_bus = bus;
        }
    }

    println!("{} departing at {}", min_bus, min_time + timestamp);

    println!("{}", min_time * min_bus);


    // Part 2. Was pretty clueless and needed many hints here.
    // Never heard of the "Chinese Remainder Theorem," but
    // that's apparently what you're supposed to implement.
    // I still don't really understand it tbh.

    let mut bus_pairs: Vec<(i64, i64)> = Vec::new();
    for (ii, split) in buses.split(",").enumerate() {
        if split != "x" {
            let id: i64 = split.parse().unwrap();
            let i: i64 = ii as i64;

            // % in Rust is remainder and *not* modulus (why???)
            // So we have to use ((a % b) + b) % b)
            bus_pairs.push((id, (((id - i) % id) + id) % id));
            println!("{}: {}", id, (((id - i) % id) + id) % id);
        }
    }


    // Sieve method as described on Wikipedia
    let (mut n, mut x) = bus_pairs[0];

    for ii in 1..bus_pairs.len() {
        let (id, modulus) = bus_pairs[ii];
        loop {
            x += n;
            if ((x % id) + id) % id == modulus {
                break;
            }
        }
        n *= id;
    }

    println!("{}", x);
}

