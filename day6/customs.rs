use std::env;
use std::fs;
use std::io::{self, BufRead};
use std::collections::HashSet;

fn main() {
    let args: Vec<String> = env::args().collect();

    let filename: &String = &args[1];
    let file = fs::File::open(filename).expect("Unable to open file");
    let reader = io::BufReader::new(file);

    let mut total_answered_questions: i32 = 0;
//    let mut total_group_intersection: i32 = 0;
    let mut ss: String = "".to_owned();
//    let mut char_sets: Vec<HashSet<char>> = Vec::new();
    for line in reader.lines() {
        let text = line.unwrap();

        if text.eq("") {
            let unique_chars: i32 = count_unique_chars(&ss);
            total_answered_questions += unique_chars;

//            let group_intersection_count: i32 = group_answer_intersection(char_sets);
//            total_group_intersection += group_intersection_count;

//            char_sets = Vec::new();
            ss = "".to_string();
        }
        else {
            ss.push_str(&text);
            // Another copy probably?
//            char_sets.push(make_char_set(&ss));
        }
    }

    if ss != "" {
        total_answered_questions += count_unique_chars(&ss);
    }

//    if char_sets.len() > 1 {
//        total_group_intersection += group_answer_intersection(char_sets);
//    }

    println!("Total unique answered questions: {}", total_answered_questions);
//    println!("Total group intersection answers: {}", total_group_intersection);
}

// I'm guessing this probably triggers a copy which means it's inefficient.
// Should consider Box for heap allocation maybe?
//fn make_char_set(in_str: &String) -> HashSet<char> {
//    let mut set: HashSet<char> = HashSet::new();
//
//    for ch in in_str.chars() {
//        set.insert(ch);
//    }
//
//    return set;
//}

//fn group_answer_intersection(group_answers: Vec<HashSet<char>>) -> i32 {
//    // Not how I was wanting to write intersection of multiple sets since
//    // the rest of the code is non-functional, but this is definitely the
//    // nicest way imo.
//
//    let iter = group_answers.iter();
//    let intersection = iter
//                       .next()
//                       .iter()
//                       .map(|set| iter.fold(set, |set1, set2| set1.intersection(set2).collect()))
//                       .collect();
//    let mut common_answers: HashSet<char> = group_answers.pop().unwrap();
//    for set in group_answers {
//        common_answers = common_answers.iter().filter(|ch| set.contains(*ch)).cloned().collect();
//    }
//    return intersection.len() as i32;
//}

fn count_unique_chars(to_count: &String) -> i32 {
    let mut set: HashSet<char> = HashSet::new();

    for ch in to_count.chars() {
        set.insert(ch);
    }

    return set.len() as i32;
}
