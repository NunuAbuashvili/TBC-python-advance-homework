import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class AcademicPerformanceAnalyser:
    """
    A class to analyze academic performance data from a CSV file.
    """

    def __init__(self, csv_file_path: str):
        """
        Initialize the AcademicPerformanceAnalyser with data from a CSV file.

        :param csv_file_path: Path to the CSV file containing student data.
        """
        try:
            self.df = pd.read_csv(csv_file_path)
            self.subjects = list(self.df.columns[2:])
        except FileNotFoundError:
            print(f"Error: '{csv_file_path}' file not found.")
            raise
        except pd.errors.EmptyDataError:
            print(f"Error: '{csv_file_path}' file is empty.")
            raise
        except pd.errors.ParserError:
            print(f"Error: Unable to parse '{csv_file_path}' file.")
            raise

    def get_students_who_failed_subject(self) -> list[str]:
        """
        Identify students who have failed at least one subject.

        :return: A list of students who have failed at least one subject.
        """
        failed_subjects_filter = self.df[self.subjects] < 50
        failed_students = self.df[failed_subjects_filter.any(axis='columns')]['Student'].unique()
        return failed_students

    def get_highest_gpa_students(self) -> tuple:
        """
        Find students with the highest GPA across all subjects and semesters.

        :return: A tuple containing a list of students with the highest GPA and their GPA.
        """
        student_average_scores = (
            self.df.groupby(by='Student')[self.subjects].mean().mean(axis='columns')
        )
        highest_average_score = student_average_scores.max()
        highest_gpa_students = (
            student_average_scores[student_average_scores == highest_average_score].index.tolist()
        )
        return highest_gpa_students, highest_average_score

    def get_subject_with_lowest_average_score(self) -> str:
        """
        Find the subject with the lowest average score across all semesters.

        :return: The name of the subject with the lowest average score.
        """
        subject_average_scores = self.df[self.subjects].mean()
        subject_with_lowest_average_score = subject_average_scores.idxmin()
        return subject_with_lowest_average_score

    def generate_and_save_average_scores_data(self, output_file_path: str):
        """
        Generate average scores data and save it to an Excel file.

        :param output_file_path: Path to save the Excel file.
        """
        try:
            average_scores_per_semester = (
                self.df.groupby(by='Semester')[self.subjects].mean().round(2)
            )
            average_scores_per_semester.to_excel(output_file_path, sheet_name='Average Scores')
            print(f"\nAverage scores data saved to '{output_file_path}'.")
        except PermissionError:
            print(f"Error: No permission to write to file '{output_file_path}'")
            raise

        return average_scores_per_semester

    def get_students_with_consistent_progress(self) -> list[str]:
        """
        Identify students who have consistently improved their grades across semesters.

        :return: A list of students with consistently improving grades.
        """
        average_scores_per_subject = self.df.groupby(['Student', 'Semester'])[self.subjects].mean()
        average_scores_per_semester = average_scores_per_subject.mean(axis='columns').unstack()

        def is_consistently_improving(scores):
            return all(scores.iloc[i] < scores.iloc[i+1] for i in range(len(scores)-1))

        students_consistently_improving = (
            average_scores_per_semester[average_scores_per_semester.
            apply(is_consistently_improving, axis='columns')].
            index.tolist()
        )

        return students_consistently_improving

    def create_average_score_bar_graph(self, output_file_path: str):
        """
        Create a bar graph showing the average score per subject across all semesters.

        :param: Path to save the bar chart image.
        """
        try:
            average_scores = self.df[self.subjects].mean().sort_values(ascending=False)
            highest_average_score = average_scores.max()

            fig, ax = plt.subplots(figsize=(10, 6))
            plt.bar(self.subjects, average_scores, color='#A0D683', width=0.6)
            ax.set_xlabel('Subjects', labelpad=15)
            ax.set_ylabel('Average Score', labelpad=15)
            ax.set_title('Average Score per Subject Through all Semesters', pad=15,
                         fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontfamily': 'serif'})

            ax.set_yticks(np.arange(0, int(highest_average_score + 10), 5))
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            plt.savefig(output_file_path, dpi=300)
            plt.close()
            print(f"\nBar chart saved to '{output_file_path}'.")
        except PermissionError:
            print(f"Error: No permission to write to file '{output_file_path}'.")
            raise

    def create_average_score_line_graph(self, output_file_path: str) -> None:
        """
        Create a line graph showing the average overall score by semester.

        :param: Path to save the line graph image.
        """
        try:
            average_scores_by_semester = (
                self.df.groupby('Semester')[self.subjects].mean().mean(axis='columns')
            )
            semesters = sorted(self.df['Semester'].unique())

            fig, ax = plt.subplots(figsize=(10, 6))
            plt.plot(semesters, average_scores_by_semester)
            ax.set_xlabel('Semester', labelpad=15)
            ax.set_ylabel('Average Score', labelpad=15)
            ax.set_title('Average Overall Score by Semester', pad=15,
                         fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontfamily': 'serif'})
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()

            plt.savefig(output_file_path, dpi=300)
            plt.close()
            print(f"Line graph saved to '{output_file_path}'.")
        except PermissionError:
            print(f"Error: No permission to write to file '{output_file_path}'.")
            raise


def main():
    """ Main function to run the program and print results. """
    csv_file = 'student_scores_random_names.csv'
    excel_file = 'average_scores_per_subject.xlsx'
    bar_chart_file = 'average_score_per_subject.png'
    line_graph_file = 'average_score_by_semester.png'
    data_processor = AcademicPerformanceAnalyser(csv_file)

    students_who_failed = data_processor.get_students_who_failed_subject()
    print(f"There are {len(students_who_failed)} students who have failed at least one subject. "
          f"Those students are: {', '.join(sorted(students_who_failed))}")

    average_scores_per_semester = data_processor.generate_and_save_average_scores_data(excel_file)
    print(f"\nAverage score of each subject per semester: \n{average_scores_per_semester}")

    highest_gpa_students, highest_gpa = data_processor.get_highest_gpa_students()
    print(f"\nStudent(s) with the highest average score "
          f"({highest_gpa}): {', '.join(highest_gpa_students)}.")

    hardest_subject = data_processor.get_subject_with_lowest_average_score()
    print(f"\nSubject with the lowest average score across all semesters is {hardest_subject}.")

    students_with_progress = data_processor.get_students_with_consistent_progress()
    if students_with_progress:
        print(f"\nStudents with consistently improving grades: {', '.join(students_with_progress)}")
    else:
        print("\nThere are no students who have consistently improved their grades.")

    data_processor.create_average_score_bar_graph(bar_chart_file)
    data_processor.create_average_score_line_graph(line_graph_file)


if __name__ == '__main__':
    main()
