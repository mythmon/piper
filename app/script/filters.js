(function() {

  var module = angular.module('piper');

  module.filter('money', function() {
    return function(input) {
      var negative = (input <= -0.01);
      var intPart = Math.floor(Math.abs(input));
      var decPart = (Math.abs(input) - intPart).toFixed(2);

      var out = negative ? '-$' : '+$';
      out += intPart + '.' + decPart.toString().slice(-2);

      return out;
    }
  });

})();