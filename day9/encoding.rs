use std::env;
use std::fs;
use std::io::{self, BufRead};

static WINDOW_SIZE: usize = 25;

fn main() {
    let args: Vec<String> = env::args().collect();

    let filename = &args[1];
    let file = fs::File::open(filename).expect("Unable to open file");
    let reader = io::BufReader::new(file);

    let mut code: Vec<u64> = Vec::new();
    for line in reader.lines() {
        let text = line.unwrap();
        let num: u64 = text.parse().unwrap();  // lol...
        code.push(num);
    }

    let bad_val: u64 = check_slices(&code[0..WINDOW_SIZE], &code, 0);
    println!("{}", bad_val);

    let range_sum: u64 = find_range_sum(&code, &bad_val);
    println!("{}", range_sum);
}

fn check_slices<'a>(window: &'a [u64], haystack: &'a Vec<u64>, idx: usize) -> u64 {
    if idx + WINDOW_SIZE == haystack.len() {
        return 0;
    }

    for ii in 0..window.len() {
        for jj in 0..window.len() {
            if ii == jj {
                continue;
            }
            if window[ii] + window[jj] == haystack[idx + WINDOW_SIZE] {
                let next: usize = idx + 1;
                return check_slices(&haystack[next..(next + WINDOW_SIZE)], haystack, next);
            }
        }
    }

    return haystack[idx + WINDOW_SIZE];
}

fn find_range_sum(haystack: &Vec<u64>, target: &u64) -> u64 {
    let mut sum: u64 = 0;
    let mut vals: Vec<u64> = Vec::new();
    for ii in 0..haystack.len() {
        let mut idx = ii;
        while sum < *target {
            sum += haystack[idx];
            vals.push(haystack[idx]);
            idx += 1;
        }

        if sum == *target {
            vals.sort();
            return vals[0] + vals[vals.len()-1];
        }
        else {
            sum = 0;
            vals.clear();
        }
    }

    return 0;
}
