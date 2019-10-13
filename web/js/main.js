		$(function(){
			var place = 'Bengaluru';
			$('#submit').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
			$('#submit').attr('disabled',true);
			$('#place').attr('placeholder','Wait a second');
			$.post('/daily',{'place' : place})
			.done(function(data){
					var data = JSON.parse(data);
					$.each(data,function(index,value){
						$('#'+index).html(value);
					});
					hourly(place);
					monthly(place);
					$('#place').attr('placeholder','Enter the Place Name');
			})
			.fail(function(data){
					alert('Invalid Name');
					$('#submit').html('Submit');
					$('#submit').attr('disabled',false);
			});
		});
		$('form#myform').submit(function(e){
			e.preventDefault();
			var place = $('#place').val();
			$('#submit').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...');
			$('#submit').attr('disabled',true);
			console.log(place);
			$.ajax({
				type: "POST",
				url: '/daily',
				data: {'place' : place},
				success : function(data,textStatus,xhr){
					var data = (JSON.parse(data));
					$.each(data,function(index,value){
						$('#'+index).html(value);
					});
					monthly(place);
					hourly(place);
				},
				error : function(data,textStatus,xhr){
					alert('Invalid Name');
					$('#submit').html('Submit');
					$('#submit').attr('disabled',false);
				}
			}); 			

		});

	function hourly(place){
			$.ajax({
				type: "POST",
				url: '/hourly',
				// aysnc: true,
				data: {'place' : place},
				success : function(data){
					var data = (JSON.parse(data));
					$('#hourly_tab').empty();
					$.each(data['hourly'],function(index,value){
						$('#hourly_tab').append('<tr>');
						$.each(value,function(ind,val){
							$('#hourly_tab').append('<td>'+val+'</td>');
						});
						$('#hourly_tab').append('</tr>');
					});

				}
			});
	}	

	function monthly(place){
			$.ajax({
				type: "POST",
				url: '/monthly',
				// aysnc: true,
				data: {'place' : place},
				success : function(data){
					var data = (JSON.parse(data));
					console.log(data);
					$('#monthly_tab').empty();
					$.each(data['monthly'],function(index,value){
						$('#monthly_tab').append('<tr>');
						$.each(value,function(ind,val){
							$('#monthly_tab').append('<td>'+val+'</td>');
						});
						$('#monthly_tab').append('</tr>');
					});
					$('#submit').html('Submit');
					$('#submit').attr('disabled',false);

				}
			});		
	}