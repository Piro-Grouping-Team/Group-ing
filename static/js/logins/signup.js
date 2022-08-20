const form_check = () => {
  const userId = document.getElementById("user_id");
  const userPw1 = document.getElementById("user_password1");
  const userPw2 = document.getElementById("user_password2");
  //   const userName = document.getElementById(user_name);
  //   const userNickName = document.getElementById(user_nickname);
  //   const email = document.getElementById(user_email);
  //   const phoneNum = document.getElementById(user_phonenum);
  //   const userAge = document.getElementById(user_age);
  //   const address1 = document.getElementById(user_address1);
  //   const address2 = document.getElementById(user_address2);
  //   const gender = document.getElementById(user_gender);
  //   const userImg = document.getElementById(user_img);

  const pwCheck = /^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{8,25}$/;

  if (len(userId.value) < 5) {
    alert("아이디를 5자 이상 적어주세요!");
    userId.focus();
    return false;
  }

  if (!pwCheck.test(userPw1.value)) {
    alert("비밀번호는 영문자+숫자+특수문자 조합으로 8-25자리 사용해야 합니다.");
    userPw1.focus();
    return false;
  }

  if (userPw1.value !== userPw2.value) {
    alert("비밀번호가 일치하지 않습니다");
    userPw2.focus();
    return false;
  }

  document.form_check.submit();
};
