



document.getElementById("buton").addEventListener("click", getInfo);

function getInfo()
{
    let info = document.getElementById("text").value;
    console.log(info);
    document.getElementById("text").value = "";
    $.ajax({
        type: "POST",
        url: "/receiver",
        contentType: "json",
        dataType: "json",
        data: JSON.stringify({"location": info}),
        success: function(response) {
            console.log(response);
        },
        error: function(err) {
            console.log(err);
        }
    });
    
}