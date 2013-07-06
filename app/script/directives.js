(function() {

var module = angular.module('piper');

module.directive('sortToggle', function() {
    return {
      restrict: 'E',
      replace: true,
      scope: {
        name: '=',
        value: '@'
      },

      template:
        '<span class="sort-toggle">' +
          '<button class="tiny" ng-click="changeSort(false)"' +
           'ng-class="{secondary: name != value}">^</button>' +
          '<button class="tiny" ng-click="changeSort(true)"' +
           'ng-class="{secondary: name != \'-\' + value}">v</button>' +
        '</span>',

      link: function(scope, element, attrs) {
        scope.changeSort = function(descending) {
          var order = descending ? '-' : '';
          scope.name = order + scope.value;
        };
      }
    };
  });

})();
