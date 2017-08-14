
	var canvas = document.getElementById('canvas_map')
	var canvas_parent = document.getElementById('canvas_parent')
	var ctx = canvas.getContext('2d');

	var map_img = new Image();

	map_img.src = image_src;



	window.onresize = function() {

		on_load();
	}

	window.onload = on_load();

	function on_load(){
		//initial scale canvas.width/map_img.clientWidth;

		canvas.width = canvas_parent.offsetWidth;
		canvas.height = canvas.width;

		    trackTransforms(ctx);

        redraw();

      var lastX=canvas.width/2, lastY=canvas.height/2;

      var dragStart,dragged;

      canvas.addEventListener('mousedown',function(evt){
          document.body.style.mozUserSelect = document.body.style.webkitUserSelect = document.body.style.userSelect = 'none';
          lastX = evt.offsetX || (evt.pageX - canvas.offsetLeft);
          lastY = evt.offsetY || (evt.pageY - canvas.offsetTop);
          dragStart = ctx.transformedPoint(lastX,lastY);
          dragged = false;
           set_coordinates(event);
      },false);

      canvas.addEventListener('mousemove',function(evt){
          lastX = evt.offsetX || (evt.pageX - canvas.offsetLeft);
          lastY = evt.offsetY || (evt.pageY - canvas.offsetTop);
          dragged = true;
          if (dragStart){
            var pt = ctx.transformedPoint(lastX,lastY);
            ctx.translate(pt.x-dragStart.x,pt.y-dragStart.y);
            redraw();
                }
      },false);

      canvas.addEventListener('mouseup',function(evt){
          dragStart = null;

      },false);

      var scaleFactor = 1.1;

      var zoom = function(clicks){
          var pt = ctx.transformedPoint(lastX,lastY);
          ctx.translate(pt.x,pt.y);

          factor = Math.pow(scaleFactor,clicks);

          ctx.scale(factor,factor);
          ctx.translate(-pt.x,-pt.y);
          redraw();
      }

      var handleScroll = function(evt){
          var delta = evt.wheelDelta ? evt.wheelDelta/40 : evt.detail ? -evt.detail : 0;
          if (delta) zoom(delta);
          return evt.preventDefault() && false;
      };
			var distStart = 0;
			var handleTouchStart=  function(evt) {
			  // Handle zoom only if 2 fingers are touching the screen

				if ( evt.targetTouches.length == 2) {

				 // Get event point
				 distStart =Math.sqrt((evt.touches[0].x-evt.touches[1].x) * (evt.touches[0].x-evt.touches[1].x) +(evt.touches[0].y-evt.touches[1].y) * (evt.touches[0].y-evt.touches[1].y));
				 // Calculate delta from start scale

			 }
			}
			var handleTouchStop=  function(evt) {
			  // Handle zoom only if 2 fingers are touching the screen

				if ( evt.targetTouches.length == 2) {

				 // Get event point
				 var distStop =Math.sqrt((evt.touches[0].x-evt.touches[1].x) * (evt.touches[0].x-evt.touches[1].x) +(evt.touches[0].y-evt.touches[1].y) * (evt.touches[0].y-evt.touches[1].y));
				 delta = distStop-distStart;
				 // Calculate delta from start scale
				 if (delta>0) zoom(1.2);
				 if (delta<0) zoom(-1.2);
					 return evt.preventDefault() && false;

			 }
			}
	    canvas.addEventListener('touchstart', handleTouchStart, false);
			canvas.addEventListener('touchstop', handleTouchStop, false);
	
      canvas.addEventListener('DOMMouseScroll',handleScroll, false);
      canvas.addEventListener('mousewheel',handleScroll, {passive: false});

      function set_coordinates(evt) {

				m = ctx.getTransform();
				console.log(m.a);
        var mouseX = (evt.offsetX || (evt.pageX - canvas.offsetLeft));
        var mouseY = (evt.offsetY || (evt.pageY - canvas.offsetLeft));
        newX = parseInt((mouseX   - m.e)/ m.a);
        newY = parseInt((mouseY  - m.f)/m.d);
				if( newX < 0)
				{
					newY = 1;
					newX = 1;
				}
				if( newY < 0)
				{
					newX = 1;
					newY = 1;
				}
        $("#id_x_pos").val(newX);
        $("#id_y_pos").val(newY);
      }

			start_scale = canvas.width/map_img.width;
			canvas.height = map_img.height*start_scale;
			ctx.scale(start_scale,start_scale);

			redraw();

	}





	    function redraw(){

	          // Clear the entire canvas
	          var p1 = ctx.transformedPoint(0,0);
	          var p2 = ctx.transformedPoint(canvas.width,canvas.height);
	          ctx.clearRect(p1.x,p1.y,p2.x-p1.x,p2.y-p1.y);

	          ctx.save();
	          ctx.setTransform(1,0,0,1,0,0);
	          ctx.clearRect(0,0,canvas.width,canvas.height);
	          ctx.restore();

	          ctx.drawImage(map_img,0,0);
	          for (i = 0; i < trees.length; i++) {
	            var tree = trees[i];

	            ctx.beginPath();
	            ctx.arc(tree.fields.x_pos, tree.fields.y_pos, tree.fields.radius, 0, 2 * Math.PI, false);
	            ctx.fillStyle = 'green';
	            ctx.fill();
	          }


	        }
	// Adds ctx.getTransform() - returns an SVGMatrix
	// Adds ctx.transformedPoint(x,y) - returns an SVGPoint
	function trackTransforms(ctx){
      var svg = document.createElementNS("http://www.w3.org/2000/svg",'svg');
      var xform = svg.createSVGMatrix();
      ctx.getTransform = function(){ return xform; };

      var savedTransforms = [];
      var save = ctx.save;
      ctx.save = function(){
          savedTransforms.push(xform.translate(0,0));
          return save.call(ctx);
      };

      var restore = ctx.restore;
      ctx.restore = function(){
        xform = savedTransforms.pop();
        return restore.call(ctx);
		      };

      var scale = ctx.scale;
      ctx.scale = function(sx,sy){
        xform = xform.scaleNonUniform(sx,sy);
        return scale.call(ctx,sx,sy);
		      };

      var rotate = ctx.rotate;
      ctx.rotate = function(radians){
          xform = xform.rotate(radians*180/Math.PI);
          return rotate.call(ctx,radians);
      };

      var translate = ctx.translate;
      ctx.translate = function(dx,dy){
          xform = xform.translate(dx,dy);
          return translate.call(ctx,dx,dy);
      };

      var transform = ctx.transform;
      ctx.transform = function(a,b,c,d,e,f){
          var m2 = svg.createSVGMatrix();
          m2.a=a; m2.b=b; m2.c=c; m2.d=d; m2.e=e; m2.f=f;
          xform = xform.multiply(m2);
          return transform.call(ctx,a,b,c,d,e,f);
      };

      var setTransform = ctx.setTransform;
      ctx.setTransform = function(a,b,c,d,e,f){
          xform.a = a;
          xform.b = b;
          xform.c = c;
          xform.d = d;
          xform.e = e;
          xform.f = f;
          return setTransform.call(ctx,a,b,c,d,e,f);
      };

      var pt  = svg.createSVGPoint();
      ctx.transformedPoint = function(x,y){
          pt.x=x; pt.y=y;
          return pt.matrixTransform(xform.inverse());
      }


	}
