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

    let (first, second) = find_pair(&ints[0], &ints[1..], &target_val).unwrap();

    println!("{} + {} = {}", first, second, first + second);
    println!("{} * {} = {}", first, second, first * second);
    println!("");

    let (a, b, c) = find_expense(&ints[0], &ints[1..], &target_val).unwrap();
    println!("{} + {} + {} = {}", a, b, c, a + b + c);
    println!("{} * {} * {} = {}", a, b, c, a * b * c);
}

fn find_expense<'a>(x: &'a i32, xs: &'a [i32], target: &'_ i32) -> Option<(&'a i32, &'a i32, &'a i32)> {
    if xs.len() == 0 {
        return Option::None;
    }

    if x < target {
        let rem = *target - x;
        for i in 0..(xs.len() - 1) {
            if let Some((a, b)) = find_pair(&xs[i], &xs[i+1..], &rem) {
                return Option::Some((x, a, b));
            }
        }
    }

    find_expense(&xs[0], &xs[1..], target)
}

fn find_pair<'a>(x: &'a i32, xs: &'a [i32], target: &'_ i32) -> Option<(&'a i32, &'a i32)> {
    if xs.len() == 0 {
        return Option::None;
    }

    for val in xs {
        if x + val == *target {
            return Option::Some((x, val));
        }
    }

    find_pair(&xs[0], &xs[1..], target)
}
