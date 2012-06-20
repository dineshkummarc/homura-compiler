var editor;

var run;

/* when page is ready */
$(document).ready(function(){
	editor = ace.edit("editor");
	//editor.setTheme("ace/theme/twilight");

	$('#language').on('change', function(){
		var Mode = require("ace/mode/"+$('#language > option[value="'+$(this).val()+'"]').attr('mode')).Mode;
		editor.getSession().setMode(new Mode());
		if (isNaN($('#source_name').attr('rel'))) return true;
		var sn = $('#source_name').html();
		sn = sn.match(/^([\w\d_]+)\.?.*$/)[1];
		sn = sn + '.' + $('#language > option[value="'+$(this).val()+'"]').attr('ext');
		$('#source_name').html(sn);
	});
	$('#source_name').html('Unnamed.java');
	$('#language').val('java');
	$('#language').trigger('change');

	document.getElementById("lsff_form").onsubmit=function() {
		blockUI();
		//'upload_target' is the name of the iframe
		document.getElementById('lsff_form').target = 'upload_target';
		//This function should be called when the iframe has compleated loading		
		document.getElementById("upload_target").onload = uploadDone;
	};

	var uploadDone = function(){
		unblockUI();
		var ret = frames['upload_target'].document.getElementsByTagName("body")[0].innerHTML;
		ret = ret.substr(59, ret.length - 6 - 59);
		editor.getSession().setValue(htmlDecode(ret));
		var s = $('input[name="source_file"]').val();
		var ext = s.substr(s.indexOf('.')+1, s.length);
		if (ext == 'c') $('#language').val('c');
		if (ext == 'cpp') $('#language').val('cpp');
		if (ext == 'java') $('#language').val('java');
		if (ext == 'cs') $('#language').val('csharp');
		if (ext == 'py') $('#language').val('python');
		$('#language').trigger('change');
		goToByScroll($('a[name="code"]'));
	}

	$('#input-output').hide();

	$('#compile').click(function(){
		blockUI();
		$('#report').html('');
		var source = editor.getSession().getValue();
		var language = $('#language').val();
		$.post(host+'compile', {source: source, language: language, run:run}, function(data){
			var result = $.parseJSON(data);
			var message = result.message.replace(new RegExp("\n", 'g'), '<br/>');
			$('#report').html(message);
			run = result.run;
			if (result.status == 'OK') $('#input-output').slideDown();
			unblockUI();
			goToByScroll($('a[name="report"]'));
		}).error(function(){
			unblockUI();
			$('#report').html('Server error.');
			goToByScroll($('a[name="report"]'));
		});
	});

	$('#runcode').click(function(){
		blockUI();
		var input = $('#input textarea').val();
		var language = $('#language').val();
		$.post(host+'run', {input: input, run: run, language: language}, function(data){
			var result = $.parseJSON(data);
			var output = result.output.replace(new RegExp("\n", 'g'), '<br/>');
			$('#output').html(output);
			unblockUI();
		}).error(function(a){
			unblockUI();
			console.log(a);
			$('#output').html('Server error.');
		});
	});

	// Jquery file tree
	var createTree = function(){
		$('#jqft').fileTree({ root: '/', script: '/directory', }, function(file) {
			blockUI();
			$.post('/file', {file: file}, function(data){
			var d = $.parseJSON(data);
			editor.getSession().setValue(d.body);
			$('#source_name').html(d.name);
			$('#source_name').attr('rel', d.id);
			var exp = /.*\.(\w+)$/g;
			var ext = exp.exec(d.name)[1];
			$('#language').val(ext);
			$('#language').trigger('change');
			unblockUI();
		}); });
	}

	createTree();

	$('#save').on('click', function(){
		var sourceName = $('#source_name').html();
		var sourceId = $('#source_name').attr('rel');
		$('#i_text').val(sourceName);
		if (sourceId == 0){
			$('#save_dialog').fadeIn();
			$('#overlay0').fadeIn();
			$('#i_text').focus().select();
		} else
			$('#i_button').trigger('click');
	});

	// save_dialog
	$('#i_button2').click(function(){$('#save_dialog').fadeOut();$('#overlay0').fadeOut();});
	$('#i_button').click(function(){
		blockUI();
		$('#save_dialog').fadeOut();$('#overlay0').fadeOut();
		$('#source_name').html($('#i_text').val());
		$('#language').trigger('change');

		var sourceName = $('#source_name').html();
		var sourceId = $('#source_name').attr('rel');
		var sourceCode = editor.getSession().getValue();
		$.post('/save', {name: sourceName, id: sourceId, code: sourceCode}, function(data){
			unblockUI();
			var result = parseInt(data);
			if (result == 0){
				alert('There was some error');
				return;
			}
			$('#source_name').attr('rel', result);
			createTree();
		});
	});

	// New
	$('#new').click(function(){
		$('#source_name').html('Unnamed');
		$('#language').trigger('change');
		$('#source_name').attr('rel', 0);
		editor.getSession().setValue('');
	});

	// hide loading progress after 1 sec
	setTimeout(function(){
		$('.mainloading').fadeOut();
	},0000);

});
