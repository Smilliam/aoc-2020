use std::env;
use std::fs;
use std::cmp;
use std::io::{self, BufRead};

static TOTAL_ROWS: usize = 128; // Total rows in the aircraft
static TOTAL_COLS: usize = 8;   // Total seats in any given row
static BSP_ROW_SIZE: usize = 7; // Length of the row identifier of partition string

fn main() {
    let args: Vec<String> = env::args().collect();

    let filename = &args[1];

    let file = fs::File::open(filename).expect("Unable to open file");
    let reader = io::BufReader::new(file);

    let search_space: Vec<i32> = make_search_vec(TOTAL_ROWS);

    let mut min_id: i32 = i32::MAX;
    let mut max_id: i32 = i32::MIN;
    let mut id_sum: i32 = 0;
    let mut ids: Vec<i32> = Vec::new();
    for line in reader.lines() {
        let text = line.unwrap();

        let row: i32 = get_row(&search_space[0..TOTAL_ROWS], &text[0..BSP_ROW_SIZE]);
        let col: i32 = get_col(&search_space[0..TOTAL_COLS], &text[BSP_ROW_SIZE..]);
        let id: i32 = get_seat_id(&row, &col);
        ids.push(id);
        id_sum += id;
        min_id = cmp::min(id, min_id);
        max_id = cmp::max(id, max_id);
    }

    println!("max seat id: {}", max_id);
    print_my_seat_id(&min_id, &max_id, &id_sum);
}

fn get_row<'a>(to_search: &'a [i32], row_str: &'a str) -> i32 {
    let mut row_bool: Vec<bool> = Vec::new(); 
    for ch in row_str.chars() {
        row_bool.push(ch == 'B'); 
    }

    return binary_partition(to_search, &row_bool[0], &row_bool[1..]);
}

fn get_col<'a>(to_search: &'a [i32], col_str: &'a str) -> i32 {
    let mut col_bool: Vec<bool> = Vec::new();
    for ch in col_str.chars() {
        col_bool.push(ch == 'R');
    }

    return binary_partition(to_search, &col_bool[0], &col_bool[1..]);
}

fn get_seat_id(row: &i32, col: &i32) -> i32 {
    return row * 8 + col;
}

fn binary_partition<'a>(haystack: &'a [i32], head: &'a bool, rest: &'a [bool]) -> i32 {
    if rest.len() == 0 {
        return haystack[if *head {1} else {0}];
    }

    // It feels like there should be a branchless way to do this...
    let mid: usize = haystack.len() / 2usize;
    if *head {
        return binary_partition(&haystack[mid..], &rest[0], &rest[1..]);
    }
    else {
        return binary_partition(&haystack[0..mid], &rest[0], &rest[1..]);
    }
}

fn make_search_vec(num_rows: usize) -> Vec<i32> {
    let mut v: Vec<i32> = Vec::new();
    for ii in 0..num_rows {
        v.push(ii as i32);
    }

    return v;
}

fn sum_range(start: i32, end: i32) -> i32 {
    let mut sum: i32 = 0;

    // Need an inclusive range
    for ii in start..end+1 {
        sum += ii as i32;
    }

    return sum;
}

fn print_my_seat_id(min: &i32, max: &i32, id_sum: &i32) {
    // Since we know the range will be contiguous once it
    // starts, we can take the difference between the sum
    // of the range, and the actual sum we calculated and
    // that should be our seat
    let sum_range: i32 = sum_range(*min, *max);
    println!("Your seat id is: {}", sum_range - id_sum);
}
