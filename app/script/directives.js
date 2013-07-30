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


/* Transforms an ngModel controlled date input to return milliseconds since the
 * epoch when querying it in JS. */
module.directive('unixTime', function() {
  var format = 'YYYY-MM-DD';

  return {  
    restrict: 'A',
    require: 'ngModel',
    link: function($scope, element, attrs, ngModel) {
      ngModel.$render = function() {
        toString();
      }

      function toInt() {
        var timestamp = moment(element.val(), format);
        if (timestamp !== null) {
          ngModel.$setViewValue(+timestamp);
        }
      }

      function toString() {
        if (ngModel.$viewValue !== null) {
          var timestamp = moment(ngModel.$viewValue);
          element.val(timestamp.format(format));
        }
      }

      element.bind('blur keyup change', function() {
        $scope.$apply(toInt);
      });

      toString();
    }
  };
});


module.directive('fortnight', function() {
  fortnight.watch('[fortnight]');

  return {
    restrict: 'A',
    require: 'ngModel',
  };
});


module.directive('tags', function() {
  return {
    restrict: 'A',
    require: 'ngModel',

    link: function(scope, element, attrs, ctrl) {
      ctrl.$parsers.push(function(value) {
        return _.map(value.split(/\s*,\s*/), function(t) {
          return {name: t};
        });
      });

      ctrl.$formatters.push(function(value) {
        return _.pluck(value, 'name').join(', ');
      });
    }
  };
});


module.directive('parsedSearch', function() {
  return {
    restrict: 'A',
    require: 'ngModel',

    link: function(scope, element, attrs, ctrl) {
      ctrl.$parsers.push(function(value) {
        if (value == '') {
          ctrl.$setValidity('parsed-search', true)
          return null
        }
        try {
          ctrl.$setValidity('parsed-search', true)
          return searchParser(value);
        } catch (e) {
          ctrl.$setValidity('parsed-search', false)
          ctrl.$error['parsed-search'] = e;
          return undefined;
        }
      });
    }
  };
});


})();
