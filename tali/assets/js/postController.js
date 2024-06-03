var postApp = angular.module("postApp", []);

postApp.config(function($httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});


postApp.controller("postCtrl", [
    "$scope", "$log", "$http", "$window", function($scope, $log, $http, $window) {
        $log.log("POSTAPP CONTROLLER ENTERED")
        $scope.hello = "WAHAHATS"
        $scope.createPost = function($event){

            data = {}
            data["owner"] = $scope.user
            data["content"] = $scope.post_content_text
            $log.log("CREATING POST")
            $log.log(data)

            $http({
                url: "../api/posts/",
                method: "POST",
                data: data,
                headers: {"Content-Type": "application/json"}
            }).then(function successCallback(response) {
                // this callback will be called asynchronously
                // when the response is available
                $scope.post_content_text = ""
                $window.location.reload();
              });               
    };

}]);