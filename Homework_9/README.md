# Academic Performance Analyser

## Overview

The Academic Performance Analyser is a Python-based tool designed to analyze academic performance data from a CSV file. It provides various insights into student performance across different subjects and semesters.

## Features

1. **Students Who Failed**: Identifies students who have failed at least one subject (score less than 50).
2. **Average Scores Per Semester**: Calculates the average score for each subject per semester.
3. **Highest GPA**: Finds the student(s) with the highest average GPA across all subjects and semesters.
4. **Lowest Average Subject**: Finds the subject with the lowest average score across all semesters.
5. **Students with consistent progress**: Identifies students who have consistently improved their grades across semesters.
6. **Export Average Scores**: Saves average subject scores per semester to an Excel file.
7. **Visualization**: Generates graphs for data visualization (bar graph for average scores per subject, line graph for overall average semester scores).

## Requirements

- Python 3.x
- pandas
- matplotlib
- numpy

## Installation

1. Clone this repository or download the source code.
2. Install the required packages:
    ```bash
    pip install pandas matplotlib

## Usage
1. Ensure your student data is in a CSV file named `student_scores_random_names.csv` in the same directory as the script.
2. Run the script:
    ```bash
   python main.py
3. The script will generate the following outputs:
   - Console output with various analyses.
   - An Excel file `average_scores_per_subject.xlsx` with average scores data.
   - A bar graph image `average_score_per_subject.png`.
   - A line graph image `average_score_by_semester.png`.

## Project Structure

- `student_scores_random_names.csv`: The dataset containing student scores.
- `main.py`: Main script for data analysis.
- `README.md`: Project description.
- `requirements.txt`: A list of packages or libraries needed to work on the project.
- `average_scores_per_subject.xlsx`: Excel file containing data of average scores per semester.
- `average_score_by_semester.png`: A line graph image.
- `average_score_per_subject.png` A bar graph image.

