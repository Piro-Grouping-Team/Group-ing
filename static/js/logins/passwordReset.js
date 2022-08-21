const checkForm = () => {
    const newPassword1 = document.getElementById('id_new_password1').value;
    const newPassword2 = document.getElementById('id_new_password2').value;
    if(newPassword1 == ''){
        alert('새 비밀번호를 입력해주세요!');
        newPassword1.focus();
        return false;
    }
    
    if(newPassword2 == ''){
        alert('새 비밀번호 확인을 입력해주세요!');
        newPassword2.focus();
        return false;
    }
    const pwCheck = /^(?=.*[a-z])(?=.*[A-Z])((?=.*\d)(?=.*\W)).{8,16}$/;
    if(!pwCheck.test(newPassword1)){
        alert(
            "비밀번호는 영문자+숫자+특수문자 조합으로 8-16자리를 사용해야 합니다."
        );
        newPassword1.focus();
        return false;
    }

    if (newPassword1 === newPassword2){
        alert('비밀번호가 일치하지 않습니다!');
        return false;
    }
    document.checkPwForm.submit();
}   