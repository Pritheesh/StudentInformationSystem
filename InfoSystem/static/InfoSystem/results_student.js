/**
 * Created by pritheesh on 14/03/17.
 */

function onClick(id){
    my_div = "div"+id;
    for(i = 1; i <= 4; i++)
        for(j = 1; j <= 2; j++) {
            my_other_div = "div" + i.toString() + "" + j.toString();
            if(var1 = document.getElementById(my_other_div))
                var1.style.visibility = "hidden";
        }
    document.getElementById(my_div).style.visibility = "visible";
}