function showCreate(x) {
  if (x.checked) {
    document.getElementById("FNameField").style.display = "table-row";
    document.getElementById("LNameField").style.display = "table-row";
    document.getElementById("EmailField").style.display = "table-row";
    document.getElementById("PhoneField").style.display = "table-row";
  }
}

function showRead(x) {
  if (x.checked) {
    document.getElementById("FNameField").style.display = "table-row";
    document.getElementById("LNameField").style.display = "table-row";
    document.getElementById("EmailField").style.display = "none";
    document.getElementById("PhoneField").style.display = "none";
  }
}

function showReadAll(x) {
  if (x.checked) {
    document.getElementById("FNameField").style.display = "none";
    document.getElementById("LNameField").style.display = "none";
    document.getElementById("EmailField").style.display = "none";
    document.getElementById("PhoneField").style.display = "none";
  }
}

function submitForm() {
  if (document.getElementById("CreateChecked").checked) {
    if (!document.getElementById("EmailInput").value.includes("@")) {
      alert("Must be a valid email address format!");
      return
    }
    if (isNaN(document.getElementById("PhoneInput").value)) {
      alert("Numbers only!");
      return
    }
    $.ajax({
      url: "/create-contact",
      type: "POST",
      data: JSON.stringify({
        first_name: document.getElementById("FNameInput").value,
        last_name: document.getElementById("LNameInput").value,
        email: document.getElementById("EmailInput").value,
        phone: document.getElementById("PhoneInput").value
      }),
      dataType: "text",
      contentType: 'application/json',
      success: (response, textStatus, jqXHR) => {
        $("#result").html("User added!");
      },
      error: (jqXHR, textStatus, errorThrown) => {
        $("#result").html("ERROR! User creation failed!");;
      }
    });
  } else if (document.getElementById("ReadChecked").checked) {
    $.ajax({
      url: "/read-contact",
      type: "POST",
      data: JSON.stringify({
        first_name: document.getElementById("FNameInput").value,
        last_name: document.getElementById("LNameInput").value
      }),
      dataType: "text",
      contentType: 'application/json',
      success: (response, textStatus, jqXHR) => {
        if (response !== "[]") {
          $("#result").html(
            document.getElementById("result").innerHTML =
            "<table><tr><td><b>First Name</b></td><td>" + response.split(",")[1].split('"')[1] + "</td></tr>" +
            "<tr><td><b>Last Name</b></td><td>" + response.split(",")[2].split('"')[1] + "</td></tr>" +
            "<tr><td><b>Email</b></td><td>" + response.split(",")[3].split('"')[1] + "</td></tr>" +
            "<tr><td><b>Phone</b></td><td>" + response.split(",")[4].split('"')[1] + "</td></tr>" +
            "</table>"
          );
        } else {
          $("#result").html("ERROR! Contact not found!");
        }
      },
      error: (jqXHR, textStatus, errorThrown) => {
        $("#result").html("ERROR! Contact not found!");
      }
    });
  } else if (document.getElementById("ReadAllChecked").checked) {
    $.ajax({
      url: "/read-all-contacts",
      type: "GET",
      success: (response, textStatus, jqXHR) => {
        if (response !== "[]") {
          var output = "";
          for (var i = 0; i < response.length; i++) {
            output +=
              "<table border=\"1px solid black\"><tr><td><b>First Name</b></td><td>" + response[i][1] + "</td></tr>" +
              "<tr><td><b>Last Name</b></td><td>" + response[i][2] + "</td></tr>" +
              "<tr><td><b>Email</b></td><td>" + response[i][3] + "</td></tr>" +
              "<tr><td><b>Phone</b></td><td>" + response[i][4] + "</td></tr>" +
              "</table><br/>";
          }
          $("#result").html(output);
        } else {
          $("#result").html("ERROR! Contacts not found!");
        }
      },
      error: (jqXHR, textStatus, errorThrown) => {
        $("#result").html("ERROR! Contacts not found!");
      }
    });
  }
}