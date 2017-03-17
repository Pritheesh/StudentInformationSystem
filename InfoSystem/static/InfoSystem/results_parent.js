/**
 * Created by pritheesh on 15/03/17.
 */

function onClick(stud, ei){
    my_div = "div"+stud+ei;
    // console.log(hall);
    // console.log(id);
    for(i = 1; i <= 4; i++)
        for(j = 1; j <= 2; j++) {
            my_other_div = "div" + stud + i.toString() + "" + j.toString();
            if(var1 = document.getElementById(my_other_div))
                var1.style.visibility = "hidden";
        }
    document.getElementById(my_div).style.visibility = "visible";
}

function onClickOuter(stud){
    outer_div = "div"+stud;
    console.log(outer_div);
    for(i = 1; i <= 10; i++){
        my_other_div = "div" + i.toString();
        if((var1 = document.getElementById(my_other_div)) !=  null) {
            console.log(var1);
            if(i != stud)
                var1.style.visibility = "hidden";
            // if(i != stud)
            for (j = 1; j <= 4; j++)
                for (k = 1; k <= 2; k++) {
                    if ((var1 = document.getElementById(my_other_div + j.toString() + k.toString()))!=null)
                        var1.style.visibility = "hidden";
                }
        }
        else
            break;
    }
    document.getElementById(outer_div).style.visibility = "visible";
    document.getElementById(outer_div+"11").style.visibility = "visible";
}