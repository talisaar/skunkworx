var signUpApp = angular.module("signUpApp", [])

signUpApp.config(function($httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

signUpApp.controller("signUpCtrl", [
    "$scope", "$log", "$http", function($scope, $log, $http) {
    
    $scope.angular_string = "my Angular string"
    $scope.ready = false
    $scope.newUser = {}

    
    $scope.signUp = function($event){

        if (($scope.password) != ($scope.password_confirm)) {
            $log.info("detected mismatching passwords")
            return
        }
        
        data = {}
        data["username"] = $scope.email
        data["password"] = $scope.password
        data["firstname"] = $scope.firstname
        data["lastname"] = $scope.lastname
        data["email"] = $scope.email
        $log.info(data)
        $scope.ready = true

    if ($scope.ready){
        $log.info("READY to sign up")

        $http({
                url: "api/users/",
                method: "POST",
                data: data,
                headers: {"Content-Type": "application/json"}
            })
    }
    else{
            $log.info("not ready to sign up")
    }}
  }]);
