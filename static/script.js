



document.getElementById("sendData").addEventListener("click", getInfo);

function getInfo()
{
    console.log("merge");
    let sendData = {
        product : document.getElementById("product").value,
        quantity : document.getElementById("quantity").value,
        price : document.getElementById("price").value

    };
    //reinit formulare
    document.getElementById("product").value = "";
    document.getElementById("quantity").value = "";
    document.getElementById("price").value = "";
    $.ajax({
        type: "POST",
        url: "/post",
        contentType: "application/json",
        data: JSON.stringify(sendData),
        dataType: "json",
        success: function(response) {
            console.log(response);
        },
        error: function(err) {
            console.log(err);
        }
    });
    
}