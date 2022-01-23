var PointCalibrate = 0;
var CalibrationPoints={};

function ClearCanvas(){
  $(".Calibration").hide();
  var canvas = document.getElementById("plotting_canvas");
  canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
}
function PopUpInstruction(){
  ClearCanvas();
  swal({
    title:"Eye Gaze Pattern",
    text: "Please click on each of the 6 points on the screen. Repeat at least 5 times to calibrate for each step.",
    buttons:{
      cancel: false,
      confirm: true
    }
  }).then(isConfirm => {
    ShowCalibrationPoint();
  });

}
function helpModalShow() {
    $('#helpModal').modal('show');
}
$(document).ready(function(){
  ClearCanvas();
  helpModalShow();
     $(".Calibration").click(function(){

      var id = $(this).attr('id');

      if (!CalibrationPoints[id]){
        CalibrationPoints[id]=0;
      }
      CalibrationPoints[id]++;
      console.log(CalibrationPoints)

      if (CalibrationPoints[id]==5){
        $(this).css('background-color','yellow');
        $(this).prop('disabled', true);
        PointCalibrate++;
      }else if (CalibrationPoints[id]<5){
        var opacity = 0.2*CalibrationPoints[id]+0.2;
        $(this).css('opacity',opacity);
      }

      

      if (PointCalibrate >= 5){ 
            $(".Calibration").hide();
            $("#Pt5").show();

            var canvas = document.getElementById("plotting_canvas");
            canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);

            swal({
              title: "Setting up your password",
              text: "Look at the dot to calibrate.",
              closeOnEsc: false,
              allowOutsideClick: false,
              closeModal: true
            }).then( isConfirm => {
                $(document).ready(function(){

                  store_points_variable();

                  sleep(5000).then(() => {
                      stop_storing_points_variable();
                      var past50 = webgazer.getStoredPoints();
                      var precision_measurement = calculatePrecision(past50);
                      var accuracyLabel = "<a>Password Strength | "+precision_measurement+"%</a>";
                      document.getElementById("Accuracy").innerHTML = accuracyLabel;
                      swal({
                        title: "Your password strength is" + precision_measurement + "%",
                        allowOutsideClick: false,
                        buttons: {
                          cancel: "Try again",
                          confirm: true,
                        }
                      }).then(isConfirm => {
                          if (isConfirm){
                            ClearCanvas();
                          } else {
                            document.getElementById("Accuracy").innerHTML = "<a>Setup in progress</a>";
                            webgazer.clearData();
                            ClearCalibration();
                            ClearCanvas();
                            ShowCalibrationPoint();
                          }
                      });
                  });
                });
            });
          }
    });
});

function ShowCalibrationPoint() {
  $(".Calibration").show();
}

function ClearCalibration(){

  $(".Calibration").css('background-color','red');
  $(".Calibration").css('opacity',0.2);
  $(".Calibration").prop('disabled',false);

  CalibrationPoints = {};
  PointCalibrate = 0;
}

function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}
