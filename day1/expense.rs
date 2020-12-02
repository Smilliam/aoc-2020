use std::env;
use std::fs;
use std::io::{self, BufRead};

fn main() {
    let args: Vec<String> = env::args().collect();

    let filename = &args[1];
    let target_val: i32 = args[2].parse().unwrap();

    let file = fs::File::open(filename).expect("Unable to open file");
    let reader = io::BufReader::new(file);

    let mut ints = Vec::new();
    for line in reader.lines() {
        let text = line.unwrap();
        let int: i32 = text.parse().unwrap();
        ints.push(int);
    }

    ints.sort();

    let (first, second) = find_sum_vals(&ints, target_val);

    println!("{} {}", first, second);
    println!("{}", first * second);
}

fn find_sum_vals(ints: &Vec<i32>, target: i32) -> (i32, i32) {
    for big in ints.iter().rev() {
        for small in ints.iter() {
            if small > big {
                break;
            }
            else if small + big == target {
                return (*small, *big);
            }
        }
    }

    return (0, 0);
}
