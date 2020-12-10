use std::env;
use std::fs;
use std::io::{self, BufRead};
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;

fn main() {
    let args: Vec<String> = env::args().collect();

    let filename = &args[1];
    let file = fs::File::open(filename).expect("Unable to open file");
    let reader = io::BufReader::new(file);

    let mut joltages: Vec<i32> = Vec::new();
    let mut joltage_set: HashSet<i32> = HashSet::new();
    joltages.push(0);
    for line in reader.lines() {
        let text = line.unwrap();
        let joltage: i32 = text.parse().unwrap();
        joltages.push(joltage);
        joltage_set.insert(joltage);
    }
    joltages.sort();

    // This needs to happen *after* the sort or else you don't actually
    // get the right value and you spend half a hour debugging dumb values.
    joltages.push(joltages[joltages.len()-1] + 3);

    let mut joltage_map: HashMap<i32, i32> = HashMap::new();

    let mut prev: i32 = 0;
    for ii in 0..joltages.len() {
        let diff: i32 = joltages[ii] - prev;
        let joltage = joltage_map.entry(diff).or_insert(0);
        *joltage += 1;
        prev = joltages[ii];
    }
    println!("{}", joltage_map.get(&1).unwrap() * *joltage_map.get(&3).unwrap());

    // Wow, dynamic programming
    let mut perm_counts: Vec<u64> = Vec::new();
    perm_counts.push(1);
    for ii in 1..joltages.len() {
        let mut count: u64 = 0;
        for jj in 0..ii {
            if joltages[jj] + 3 >= joltages[ii] {
                count += perm_counts[jj];
            }
        }
        perm_counts.push(count);
    }
    println!("num valid: {}", perm_counts[perm_counts.len() - 1]);
}
