//<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

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
    document.getElementById("popUp").style.display = "none"
    if (sendData[product] == '')
        return;
        
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