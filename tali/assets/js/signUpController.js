var signUpApp = angular.module("signUpApp", []);

signUpApp.config(function($httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

signUpApp.controller("signUpCtrl", [
    "$scope", "$log", "$http", "$window", function($scope, $log, $http, $window) {
    
    $log.log("SIGNUPAPP CONTROLLER ENTERED")
    $scope.angular_string = "my Angular string"
    $scope.hide_button = false
    $scope.hide_processing_text = true
    $scope.ready = false
    $scope.newUser = {}
    $scope.error_msg = ""
    $scope.signUp = function($event){
        
        $scope.error_msg = ""
        if ($scope.email && $scope.firstname && $scope.lastname && $scope.password && $scope.password_confirm) {
            // Verify passwords match 
            $log.info("all required fields exist!")
            if (($scope.password) != ($scope.password_confirm)) {
                $log.info("detected mismatching passwords")
                return
            }
        }
        else {
            $log.info("missing fields")
            return
        }
        
        // Disable button and show text to avoid multiple submits 

        $scope.hide_button = true
        $scope.hide_processing_text = false

        // Prep Http request data 

        data = {}
        data["username"] = $scope.email
        data["password"] = $scope.password
        data["firstname"] = $scope.firstname
        data["lastname"] = $scope.lastname
        data["email"] = $scope.email

        // Post data to create user 

        $http({
                    url: "api/users/",
                    method: "POST",
                    data: data,
                    headers: {"Content-Type": "application/json"}
                }).then(function successCallback(response) {
                    // this callback will be called asynchronously
                    // when the response is available

                    // Display check_email screen and pass email address as param
                    $scope.url_str = 'check_email/?email=' + $scope.email
                    $window.location = $window.location.href + $scope.url_str
                  }).catch(function(error)  {
                    $scope.hide_button = false
                    $scope.hide_processing_text = true

                    if (error.data.includes("duplicate key value violates unique constraint")) {
                        $scope.error_msg = 'email already exists'
                    }
                    else {
                        $scope.error_msg = 'Oh skunks! Something went wrong'
                    } 
                    })     
    };
    $scope.send_activation = function(email){
        data = {}
        data["email"] = email

        $http({
            url: "../send_activation/",
            method: "POST",
            data: data,
            headers: {"Content-Type": "application/json"}
        }).catch(function(error) {
            $log.info("Something went wrong with sending activation email")
        })

    };

}]);
