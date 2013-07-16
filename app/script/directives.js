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


/* Transforms an ngModel controlled date input to return seconds since the
 * epoch when querying it in JS. */
module.directive('unixTime', function() {
  var format = 'YYYY-MM-DD';

  return {  
    restrict: 'A',
    require: 'ngModel',
    link: function(scope, element, attrs, ngModel) {
      ngModel.$render = function() {
        toString();
      }

      function toUnix() {
        var timestamp = moment(element.val(), format);
        if (timestamp === null) {
          ngModel.$setViewValue(null);
        } else {
          ngModel.$setViewValue(timestamp.unix());
        }
      }

      function toString() {
        if (ngModel.$viewValue === null) {
          element.val('');
        } else {
          var timestamp = moment.unix(ngModel.$viewValue);
          element.val(timestamp.format(format));
        }
      }

      element.bind('blur keyup change', function() {
        scope.$apply(toUnix);
      });

      toUnix();
    }
  };
});


module.directive('fortnight', function() {
  fortnight.watch('[fortnight]');

  return {
    restrict: 'A',
    require: '?ngModel',
  };
});

})();
