from InfoSystem.models import *
import sys

# semester wise
ei = ExamInfo.objects.all().filter(supple=False)

for i in range(1, 5):
    for j in range(1, 3):
        sem = ei.filter(year_of_pursue=i, semester=j)
        results_total = []
        for p in sem:
            results_total.append(int(p.total))
            # results_total[p] = int(p.total)
            #results_total.append({p.student: int(p.total)})
        if results_total != []:
            results_total= list(set(results_total))
            results_total.sort(reverse=True)
            # results_total = sorted(results_total.items(), key= lambda x:x[1], reverse=True)
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


