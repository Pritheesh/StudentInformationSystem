from InfoSystem.models import *
import sys

# semester wise

def insert_sem_ach(year_of_pursue, year_of_calendar, semester, month_of_year):
    sem = ExamInfo.objects.filter(year_of_calendar=year_of_calendar, year_of_pursue=year_of_pursue,
                                  month_of_year=month_of_year, semester=semester, supple=False)
    results_total = []
    for p in sem:
        results_total.append(int(p.total))
    if results_total != []:
        results_total = list(set(results_total))
        results_total.sort(reverse=True)
        try:
            temp = sem.filter(total=results_total[0])
            for lmn in temp:
                achievement_in_semester = AchievementInASemester(rank=1, student=lmn.student, examinfo=lmn)
                achievement_in_semester.save()
                print achievement_in_semester, lmn.total
        except:
            sys.exc_info()

        try:
            temp = sem.filter(total=results_total[1])
            if temp != []:
                for lmn in temp:
                    achievement_in_semester = AchievementInASemester(rank=2, student=lmn.student, examinfo=lmn)
                    achievement_in_semester.save()
                    print achievement_in_semester, lmn.total

        except:
            sys.exc_info()

    print "------INSERTED ACHIEVEMENTS OF SEMESTER SUCCESSFULLY-----"
