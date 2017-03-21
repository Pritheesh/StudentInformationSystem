/**
 * Created by pritheesh on 14/03/17.
 */

function calcPercentage(temp, id1, id2) {
    var tot = document.getElementById("total").value;
    console.log(tot);
    if ( Number(tot) <= 0)
        alert("Oh please!!");
    else {
        var per = temp / tot;
        per *= 100;
        console.log(per);
        ele = "div_total"+id1.toString()+id2.toString();
        console.log(ele);
        document.getElementById(ele).innerHTML = "Percentage: " + per;
    }
}

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