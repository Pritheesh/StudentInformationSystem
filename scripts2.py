from InfoSystem.models import Subject, Result, AchievementInASubject

subjects = Subject.objects.all()

for sub in subjects:
    results = Result.objects.filter(subject = sub)
    results = results.filter(examinfo__supple=False)
    sub_totals = []
    for res in results:
        sub_totals.append(int(res.total))
    sub_totals= list(set(sub_totals))
    sub_totals.sort(reverse=True)
    try:
        max_res = results.filter(total=sub_totals[0])
        if len(max_res) > 0:
            for lmn in max_res:
                magic = lmn.examinfo
                achievement = AchievementInASubject(rank=1, student=magic.student, result=lmn, year_of_pursue=magic.year_of_pursue,
                                                    year_of_pursue_roman=magic.year_of_pursue_roman, semester=magic.semester,
                                                    semester_roman=magic.semester_roman)
                achievement.save()
                print achievement.student.name, achievement.result.subject, achievement.result.total
                # print lmn.total, lmn.subject, lmn.examinfo.student
    except:
        print "get lost"

    try:
        max_res = results.filter(total=sub_totals[1])
        if len(max_res) > 0:
            for lmn in max_res:
                magic = lmn.examinfo
                achievement = AchievementInASubject(rank=2, student=magic.student, result=lmn,
                                                    year_of_pursue=magic.year_of_pursue,
                                                    year_of_pursue_roman=magic.year_of_pursue_roman,
                                                    semester=magic.semester,
                                                    semester_roman=magic.semester_roman)
                achievement.save()
                print achievement.student.name, achievement.result.subject, achievement.result.total
                # print lmn.total, lmn.subject, lmn.examinfo.student
    except:
        print "get lost"