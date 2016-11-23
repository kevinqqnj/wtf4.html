/*!
 * bootstrap-add-clear v1.0.7 (http://github.com/gesquive/bootstrap-add-clear)
 * Licensed under MIT (http://github.com/gesquive/bootstrap-add-clear/blob/master/LICENSE)
* modified by ezhqing@gmail.com, to work with Flask_wtf and Bootstrap4, https://github.com/kevinqqnj/wtf4.html
 */
;(function($, window, document, undefined) {

  var pluginName = "addClear";

  // The actual plugin constructor
  function Plugin(element, options) {
    this.element = element;

    this.options = $.extend({}, defaults, options);

    this._defaults = defaults;
    this._name = pluginName;

    this.init();
  }

  Plugin.prototype = {

    init: function() {
      var $this = $(this.element),
        me = this,
        options = this.options;

 //     $this.wrap("<div class='add-clear-span form-group has-feedback " + options.wrapperClass + "'></div>");
 //     $this.after($("<span class='form-control-feedback add-clear-x " + options.symbolClass + "' style='display: none;'>" + options.closeSymbol + "</span>"));
     $this.before($("<span class='add-clear-x " + options.symbolClass + "' style='display: none;'>" + options.closeSymbol + "</span>"));
// 加在 input element 前面，然后设置 css
      $this.prev().css({
        'color': options.color,
        'cursor': 'pointer',
        'text-decoration': 'none',
        'display': 'none',
        'overflow': 'hidden',
        'position': 'absolute',
        'pointer-events': 'auto',
        'right': options.right,
        'top': options.top,
        'z-index': options.zindex
      }, this);

      if ($this.val().length >= 1 && options.showOnLoad === true) {
        $this.siblings(".add-clear-x").show();
      }

      $this.on('focus.addclear', function() {
                  $(this).removeClass("form-control-danger form-control-success");
        if ($(this).val().length >= 1) {
          $(this).siblings(".add-clear-x").show();
        }
      });

      $this.on('blur.addclear', function() {
        var self = this;
        if (options.hideOnBlur) {
          setTimeout(function() {
            $(self).siblings(".add-clear-x").hide();
          }, 200);
    };
             $(this).addClass("form-control-danger form-control-success");
      });

      $this.on('keyup.addclear', function(e) {
        if (options.clearOnEscape === true && e.keyCode == 27) {
          $(this).val('').focus();
          if (options.onClear) {
            options.onClear($(this).siblings("input"));
          }
        }
        if ($(this).val().length >= 1) {
          $(this).siblings(".add-clear-x").show();
        } else {
          $(this).siblings(".add-clear-x").hide();
        }
      });

      $this.on('input.addclear change.addclear paste.addclear', function() {
        if ($(this).val().length >= 1) {
          $(this).removeClass("form-control-danger form-control-success");
          $(this).siblings(".add-clear-x").show();
        } else {
          $(this).siblings(".add-clear-x").hide();
          $(this).addClass("form-control-danger form-control-success");
        }
      });

      $this.siblings(".add-clear-x").on('click.addclear', function(e) {
 //     	  console.log($(this));
      	  $(this).val('').focus();
        $(this).siblings(me.element).val("");
        $(this).hide();
        if (options.returnFocus === true) {
          $(this).siblings(me.element).focus();
        }
        if (options.onClear) {
          options.onClear($(this).siblings("input"));
        }
        e.stopPropagation(); 
        e.preventDefault();
      });
    }

  };

 $.fn[pluginName] = function (options, optionName, optionValue) {
        return this.each(function () {
            if (options === "option") {
                var $this = $(this);
                if (optionName === "show") {
                    $this.siblings(".add-clear-x").show();
                } else if (optionName === "hide") {
                    $this.siblings(".add-clear-x").hide();
                }
            }
            var isSetOption = optionName && optionName !== "show" && optionName !== "hide";
            if (isSetOption) {
                var oldInstance = $.data(this, "plugin_" + pluginName);
                if (!oldInstance || !oldInstance.options) {
                    throw "Cannot set option, plugin was not instantiated";
                }
                oldInstance.options[optionName] = optionValue;
            } else {
                if (!$.data(this, "plugin_" + pluginName)) {
                    $.data(this,
                        "plugin_" + pluginName,
                        new Plugin(this, options));
                }
            }

        });
    };

  $.fn[pluginName].Constructor = Plugin;

  var defaults = $.fn[pluginName].defaults = {
    closeSymbol: "",
    symbolClass: 'fa fa-times-circle',
    color: "#CCC",
    top: "0.75rem",
    right: "1.0rem",
    returnFocus: true,
    showOnLoad: false,
    onClear: null,
    hideOnBlur: true,
    clearOnEscape: true,
    wrapperClass: '',
// opacity: 0.3,    	
    zindex: 100
  };

})(jQuery, window, document);

/*
Using Options

$("input").addClear({top : -2, right : 6});

// Example onClear option usage
$(":input").addClear({
  onClear: function(){
    alert("call back!");
  }
});

// Example font awesome icon usage
$(":input").addClear({
    symbolClass: "fa fa-times-circle"
})	
	*/