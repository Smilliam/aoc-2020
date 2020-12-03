use std::env;
use std::fs;
use std::io::{self, BufRead};

fn main() {
    let args: Vec<String> = env::args().collect();

    let filename = &args[1];

    let file = fs::File::open(filename).expect("Unable to open file");
    let reader = io::BufReader::new(file);

    let mut terrain: Vec<Vec<bool>> = Vec::new();
    for line in reader.lines() {
        let text = line.unwrap();
        let mut row: Vec<bool> = Vec::new();

        for ch in text.chars() {
            row.push(ch == '#');
        }

        terrain.push(row);
    }

    let mut mul_total = 1i32;
    for ii in 2..(args.len()) {
        let (x, y): (usize, usize) = parse_slope(&args[ii]).unwrap();

        let num_hit: i32 = find_num_trees_hit(&terrain, &x, &y);
        mul_total *= num_hit;
        println!("Number of trees hit with ({},{}): {}", x, y, num_hit);
    }

    println!("Multiplied total of all trees hit on every combination: {}", mul_total);
}

fn find_num_trees_hit(terrain: &Vec<Vec<bool>>, x: &usize, y: &usize) -> i32 {
    let mut num_trees_hit = 0;

    let mut x_pos: usize = 0;
    for ii in (0..(terrain.len() - 1)).step_by(*y) {
        let row: &Vec<bool> = &terrain[ii];

        if row[x_pos] {
            num_trees_hit = num_trees_hit + 1;
        }

        x_pos = (x_pos + x) % row.len();
    }

    return num_trees_hit;
}

fn parse_slope(in_str: &String) -> Option<(usize, usize)> {
    let split = in_str.split(",");
    let slope: Vec<&str> = split.collect();
    return Option::Some((slope[0].parse().unwrap(), slope[1].parse().unwrap()));
}

fn print_vec<T: std::fmt::Display>(row: &Vec<T>) {
    for printable in row.iter() {
        print!("{}", printable);
    }
    println!();
}
