/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 *
 */

"use strict";

$(document).ready(function () {
    $('.bootboxconfirm').on('click', function (e) {
        e.preventDefault();
        var hrefTo = $(this).attr('data-href');
        var dataTitle = $(this).attr('data-poptitle');
        var dataMsg = $(this).attr('data-popmsg');
        var dialog = bootbox.confirm({
            centerVertical: true,
            title: dataTitle,
            message: dataMsg,
            buttons: {
                cancel: {
                    label: '<i class="fa fa-times"></i> Cancel',
                    className: 'btn-primary'
                },
                confirm: {
                    label: '<i class="fa fa-check"></i> Confirm',
                    className: 'btn-danger'
                }
            },
            callback: function (result) {
                if (result) {
                    window.location = hrefTo;
                }
            }
        });
        dialog.on('shown.bs.modal', function () {
            dialog.find(".btn-primary:first").focus();
        });
    });

    $('.bootboxformconfirm').on('click', function (e) {
        e.preventDefault();
        var currentForm = $(this).attr('data-form');
        var dataTitle = $(this).attr('data-poptitle');
        var dataMsg = $(this).attr('data-popmsg');
        var dialog = bootbox.confirm({
            centerVertical: true,
            title: dataTitle,
            message: dataMsg,
            buttons: {
                cancel: {
                    label: '<i class="fa fa-times"></i> Cancel',
                    className: 'btn-primary'
                },
                confirm: {
                    label: '<i class="fa fa-check"></i> Confirm',
                    className: 'btn-danger'
                }
            },
            callback: function (result) {
                if (result) {
                    $('#' + currentForm).submit();
                }
            }
        });
        dialog.on('shown.bs.modal', function () {
            dialog.find(".btn-primary:first").focus();
        });
    });

    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });

    $('.openPopup').click(function () {
        var Base64 = {
            // private property
            _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
            // public method for decoding
            decode: function (input) {
                var output = "";
                var chr1, chr2, chr3;
                var enc1, enc2, enc3, enc4;
                var i = 0;

                input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

                while (i < input.length) {
                    enc1 = this._keyStr.indexOf(input.charAt(i++));
                    enc2 = this._keyStr.indexOf(input.charAt(i++));
                    enc3 = this._keyStr.indexOf(input.charAt(i++));
                    enc4 = this._keyStr.indexOf(input.charAt(i++));
                    chr1 = (enc1 << 2) | (enc2 >> 4);
                    chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
                    chr3 = ((enc3 & 3) << 6) | enc4;

                    output = output + String.fromCharCode(chr1);

                    if (enc3 != 64) {
                        output = output + String.fromCharCode(chr2);
                    }
                    if (enc4 != 64) {
                        output = output + String.fromCharCode(chr3);
                    }
                }

                output = Base64._utf8_decode(output);
                return output;
            },
            // private method for UTF-8 decoding
            _utf8_decode: function (utftext) {

                var string = "";
                var i = 0;
                var c, c2, c3;

                while (i < utftext.length) {
                    c = utftext.charCodeAt(i);

                    if (c < 128) {
                        string += String.fromCharCode(c);
                        i++;
                    }

                    else if ((c > 191) && (c < 224)) {
                        c2 = utftext.charCodeAt(i + 1);
                        string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
                        i += 2;
                    }

                    else {
                        c2 = utftext.charCodeAt(i + 1);
                        c3 = utftext.charCodeAt(i + 2);
                        string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
                        i += 3;
                    }

                }

                return string;
            }
        };

        var dataURL = $(this).attr('data-href');
        var dataIMG = $(this).attr('data-img');
        var dataLINK = $(this).attr('data-link');
        var dataSTORE = $(this).attr('data-store');
        var dataID = $(this).attr('data-id');
        var dataMPID = $(this).attr('data-mpid');
        var dataTOKEN = $(this).attr('data-token');
        var dataTOKENval = $(this).attr('data-tokenval');
        var dataTitle = $(this).attr('data-poptitle');
        var dataBase64 = $(this).attr('data-encbase64');
        var databody = '';

        $('.modal-title').html('...');
        $('.modal-body').html('<div class=text-center><div class=spinner-border role=status><span class=sr-only>Loading...</span></div></div>');

        if (dataIMG) {
            databody = "<img src='../assets/imagextra/" + dataIMG + "' class='img-fluid'>";
            
            if (dataLINK && !dataTOKEN) {
                databody = databody + "<hr><div class='text-center mt-2'><a href='index.php?hal=" + dataLINK + "&getId=" + dataID + "&getMpid=" + dataMPID + "' class='btn btn-success'>Member Detail and Manual Approval</a> <a href='javascript:;' data-dismiss='modal' class='btn btn-danger'>Dismiss</a></div>";
            }
            if (dataSTORE && !dataTOKEN) {
                databody = databody + "<hr>"
                   + "<form method='post' action='../common/sendbox.php' id='dopayform' class='mr-auto'>"
                   + "<div class='form-group mt-2 text-center'>"
                        + "<button type='submit' name='dopay' value='1' id='dopay' class='btn btn-success'>Confirm Payment and Process Order</button>"
                        + "<input type='hidden' name='sb_type' value='payreg'>"
                        + "<input type='hidden' name='sb_txitid' value='"+dataSTORE+"'>"
                        + "<input type='hidden' name='sb_amount' value='"+dataID+"'>"
                        + "<input type='hidden' name='sb_batch' value='"+dataMPID+"'>"
                        + "<input type='hidden' name='sb_label' value='Verify Approval'>"
                        + "<input type='hidden' name='sb_success' value='-ADMSALESTXAPPROVAL-'>"
                   + " <a href='javascript:;' data-dismiss='modal' class='btn btn-danger'>Dismiss</a>"
                   + "</div>"
                   + "</form>"
                   + "";
            }
            if (dataTOKEN == 'kyimgid') {
                databody = databody + "<hr><div class='text-center mt-2'>";
                if (dataTOKENval > 0) {
                    databody = databody + "<a href='index.php?hal=" + dataLINK + "&getId=" + dataID + "&getMpid=" + dataMPID + "&doKY=" + dataTOKENval + "' class='btn btn-success'>Verify Photo ID</a>";
                }
                databody = databody + " <a href='javascript:;' data-dismiss='modal' class='btn btn-danger'>Dismiss</a></div>";
            }
            
            $('.modal-title').html(dataTitle);
            $('.modal-body').html(databody);
        }
        if (dataURL) {
            $('.modal-title').html(dataTitle);
            $('.modal-body').load(dataURL, function(response, status, xhr) {
                if (status == "error") {
                var msg = "Error: ";
                    $('.modal-body').html(msg + xhr.status + " " + xhr.statusText);
                }
            });
        }
        if (dataBase64) {
            $('.modal-title').html(dataTitle);
            $('.modal-body').html(Base64.decode(dataBase64));
        }
        
        $('#myModal').modal({
            backdrop: 'static',
            keyboard: false,
            show: true
        });
        $('#myModal').on('shown.bs.modal', function() {
            $('#summernotemodal').summernote({
                height: 128,
                maxHeight: null,
                dialogsInBody: true,
                toolbar: [
                    ['font', ['bold', 'italic', 'underline', 'clear']],
                    ['view', ['codeview']]
                ]
            });
        });
    });

    $('.peppycall').on('click', function (e) {
        e.preventDefault();
        var dataKey = $("#peppyapi").val();
        
        var dataDo = $(this).attr('data-do');
        var dataValin = $(this).attr('data-valin');
        var dataOutid = $(this).attr('data-outid');
        
        var dataIsBolea = $(this).attr('data-bolea');
        var dataBoleaId = $(this).attr('data-boleaid');
        
        $.ajax({
            type: "POST",
            url: "../common/callpeppy.php",
            data: { 
                apik: dataKey,
                do: dataDo,
                valin: dataValin
            },
            success: function(response) {
                //alert(response + ' -> '+dataKey);
                // create an object with the key of the array
                var resultarr = $.parseJSON(response);
                // arrkey is the key of array that you want
                //alert(resultarr.arrkey);
       
                $("#id_" + dataOutid).html(resultarr.result1);
                if (dataIsBolea === '1' && resultarr.result2) {
                    $("#id_" + dataBoleaId).html(resultarr.result2);
                }
                //alert('ok');
            },
            error: function(response) {
                //alert('error');
            }
        });
    });
    
    var MAX_IMGFILE_SIZE = 1 * 1024 * 1024; // 5MB
    $('#uploadImgFile').change(function () {
        fileSize = this.files[0].size;
        if (fileSize > MAX_IMGFILE_SIZE) {
            this.setCustomValidity("Image file must not exceed 1Mb!");
            this.reportValidity();
        } else {
            this.setCustomValidity("");
        }
    });

    $('#summernotemini').summernote({
        height: 128,
        maxHeight: null,
        dialogsInBody: true,
        toolbar: [
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['view', ['codeview']]
        ]
    });
    $('#summernote').summernote({
        height: 256,
        maxHeight: null,
        dialogsInBody: true,
        toolbar: [
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['insert', ['link', 'picture']],
            ['view', ['fullscreen', 'codeview']]
        ]
    });
    $('#summernotemaxi').summernote({
        height: 480,
        maxHeight: null,
        dialogsInBody: true,
        toolbar: [
            ['view', ['fullscreen', 'codeview', 'undo', 'redo']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['insert', ['link', 'picture', 'video', 'hr']]
        ]
    });

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });

    var activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        $('.nav-pills a[href="' + activeTab + '"]').tab('show');
    }

    cookiesAlertBar();

});

function checkMember(agv, dataval, dataid) {
    $("#resultGetMbr" + dataid).html("<i class='fas fa-cog fa-spin'></i>");
    jQuery.ajax({
        url: "../common/index.php",
        data: 'agv=' + agv + '-' + dataval,
        type: "POST",
        success: function (data) {
            $("#resultGetMbr" + dataid).html(data);
        },
        error: function () {
        }
    });
}

function checkBoxCnt(checkboxid, showelement, toggleelement) {
    $('#' + checkboxid).change(function () {
        if (this.checked) {
            $('#' + showelement).removeClass().addClass('d-block');
            if (toggleelement)
                $('#' + toggleelement).removeClass().addClass('d-none');
            else
                $('#' + toggleelement).removeClass().addClass('d-block');
        } else {
            $('#' + showelement).removeClass().addClass('d-none');
            if (toggleelement)
                $('#' + toggleelement).removeClass().addClass('d-block');
            else
                $('#' + toggleelement).removeClass().addClass('d-none');
        }
    });
}

function getinitdo(urldo, param) {
    $("#newvernum").text('...');
    $.ajax({
        type: 'POST',
        url: urldo,
        data: "initdo=" + param,
        success: function (result) {
            var vernow = parseFloat(result);
            if (!isNaN(vernow) && vernow > 0) {
                $("#newverstr").text('New version available!');
                $("#newvernum").text('v' + vernow);
            } else {
                $("#newverstr").text('You are using the latest version!');
                $("#newvernum").text('');
            }
        }
    });
}

function dowithdrawfee(fees, fcap, cursym, withdrawfeestr, withdrawreceivestr) {
    var txamount = document.getElementById("txamount").value;
    var feestr = parseFloat(txamount) * parseFloat(fees);
    if (feestr > fcap && fcap > 0) {
        feestr = fcap;
    }
    var isfee = parseFloat(feestr).toFixed(2);
    var amount2get = parseFloat(txamount - isfee);
    document.getElementById("txamountstr1").innerHTML = withdrawfeestr + ': ' + cursym + isfee;
    document.getElementById("txamountstr2").innerHTML = withdrawreceivestr + ': ' + cursym + amount2get;
}

function cookiesAlertBar() {
    var cookieVal = 'cookieConsent';

    // Check cookie
    if (localStorage.getItem(cookieVal) != 'y')
        $('#cookieAlertBar').show();

    //Assign cookie on click
    $('#cookieAlertBarConfirm').on('click', function () {
        localStorage.setItem(cookieVal, 'y', {expires: 99}); // cookie will expire in days
        $('#cookieAlertBar').fadeOut();
    });
}

function copyInputText(idcopy) {
    /* Get the text field */
    var copyText = document.getElementById(idcopy);

    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */

    /* Copy the text inside the text field */
    document.execCommand("copy");

    /* Alert the copied text */
    //alert("Copied the text: " + copyText.value);
}

function doHideShow(isform, isval, boole, elemId) {
    var istrimval = isval.replace(' ', '');
    var isval_arr = istrimval.split("|");

    function inArray(needle, haystack) {
        var length = haystack.length;
        for (var i = 0; i < length; i++) {
            if (haystack[i] == needle)
                return true;
        }
        return false;
    }

    if (boole == true) {
        if (inArray(isform.value, isval_arr)) {
            document.getElementById(elemId).style.display = 'block';
        } else {
            document.getElementById(elemId).style.display = 'none';
        }
    } else {
        if (inArray(isform.value, isval_arr)) {
            document.getElementById(elemId).style.display = 'none';
        } else {
            document.getElementById(elemId).style.display = 'block';
        }
    }
}

function checkCountryArea(cca, dataid) {
    $("#resultGetArea" + dataid).html("+");
    jQuery.ajax({
        url: "../common/index.php",
        data: 'cca=' + cca,
        type: "POST",
        success: function (data) {
            $("#resultGetArea" + dataid).html(data);
        },
        error: function () {
        }
    });
}
