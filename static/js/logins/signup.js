let IdCheckValue = true;
let EmailCheckValue = true;

const form_check = () => {
  const userId1 = document.getElementById("id_username1");
  const userId2 = document.getElementById("id_username");
  const userPw1 = document.getElementById("id_password1");
  const userPw2 = document.getElementById("id_password2");
  const userName = document.getElementById("id_name");
  const userNickName = document.getElementById("id_nickname");
  const email1 = document.getElementById("id_email1");
  const email2 = document.getElementById("id_email");
  const phoneNum = document.getElementById("id_phoneNumber");
  const userAge = document.getElementById("id_age");
  const address1 = document.getElementById("address_kakao");
  const address2 = document.getElementById("id_addressDetail");
  //   const gender = document.getElementById("user_gender");
  //   const userImg = document.getElementById("user_img");

  // 입력 체크
  if (userId1.value == "") {
    alert("아이디를 입력하세요!");
    userId1.focus();
    return false;
  }

  if (userId1.value != "" && userId2.value == "") {
    alert("아이디 중복확인을 해주세요!");
    userId1.focus();
    return false;
  }

  if (userPw1.value == "") {
    alert("비밀번호를 입력하세요!");
    userPw1.focus();
    return false;
  }
  if (userPw2.value == "") {
    alert("비밀번호 확인을 입력하세요!");
    userPw2.focus();
    return false;
  }
  if (userName.value == "") {
    alert("이름을 입력하세요!");
    userName.focus();
    return false;
  }
  if (userNickName.value == "") {
    alert("닉네임을 입력하세요!");
    userNickName.focus();
    return false;
  }
  if (email1.value == "") {
    alert("이메일을 입력하세요!");
    email1.focus();
    return false;
  }
  if (email1.value != "" && email2.value == "") {
    alert("이메일 중복확인을 해주세요!");
    console.log(email1.value + email2.value);
    email1.focus();
    return false;
  }
  if (phoneNum.value == "") {
    alert("전화번호를 입력하세요!");
    phoneNum.focus();
    return false;
  }

  if (userAge.value == "") {
    alert("나이를 입력하세요!");
    userAge.focus();
    return false;
  }
  if (address1.value == "") {
    alert("주소를 입력하세요!");
    address1.focus();
    return false;
  }
  if (address2.value == "") {
    alert("상세주소를 입력하세요!");
    address2.focus();
    return false;
  }

  // id 길이
  if (userId1.value.length < 5 || userId1.value.length > 20) {
    alert("아이디를 5자 이상 20자 이하로 적어주세요!");
    userId1.focus();
    return false;
  }

  // 비밀번호 조건
  const pwCheck = /^(?=.*[a-z])(?=.*[A-Z])((?=.*\d)(?=.*\W)).{8,16}$/;
  if (!pwCheck.test(userPw1.value)) {
    alert(
      "비밀번호는 영문자+숫자+특수문자 조합으로 8-16자리를 사용해야 합니다."
    );
    userPw1.focus();
    return false;
  }

  // 비밀번호 일치
  if (userPw1.value !== userPw2.value) {
    alert("비밀번호가 일치하지 않습니다");
    userPw2.focus();
    return false;
  }

  // 이메일 정규식 체크
  const emailFormCheck =
    /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/;
  if (!emailFormCheck.test(email1.value)) {
    alert("이메일 형식을 지켜주세요!");
    email1.focus();
    return false;
  }

  // 아이디 중복
  if (IdCheckValue == false) {
    return false;
  }

  // 이메일 중복
  if (EmailCheckValue == false) {
    return false;
  }

  // 모두 통과하면 form 제출
  document.signupForm.submit();
};

function detectID() {
  const username1 = document.querySelector("#id_username1").value;
  const username2 = document.querySelector("#id_username").value;
  const element = document.querySelector("#error_username");
  if (username1 == username2 || username2 == "") {
    element.innerHTML = "";
  } else {
    element.innerHTML = "<p>아이디 중복확인을 해주세요!!</p>";
  }
}

function detectEmail() {
  const email1 = document.querySelector("#id_email1").value;
  const email2 = document.querySelector("#id_email").value;
  const element = document.querySelector("#error_email");
  if (email1 == email2 || email2 == "") {
    element.innerHTML = "";
  } else {
    element.innerHTML = "<p>이메일 중복확인을 해주세요!!</p>";
  }
}

// 아이디 중복체크
const usernameCheck = document.querySelector("#usernameCheck");
usernameCheck.addEventListener("click", (event) => {
  const username = document.querySelector("#id_username1").value;
  axios.defaults.xsrfCookieName = "csrftoken";
  axios.defaults.xsrfHeaderName = "X-CSRFToken";
  if (username == "") {
    alert("아이디를 입력하세요!");
    return false;
  }
  axios
    .post("/logins/signup/usernameCheck", {
      username: username,
    })
    .then((response) => {
      if (response.data.result == "fail") {
        alert("해당 아이디는 이미 존재하는 아이디입니다.");
        IdCheckValue = false;
        return false;
      } else {
        alert("사용 가능한 아이디입니다.");
        document.querySelector("#id_username").value =
          document.querySelector("#id_username1").value;
        document.querySelector("#error_username").innerHTML = "";
        return true;
      }
    });
});

// 이메일 중복체크
const emailCheck = document.querySelector("#emailCheck");
const emailForm =
  /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/;
emailCheck.addEventListener("click", (event) => {
  const email1 = document.querySelector("#id_email1");
  const email = document.querySelector("#id_email1").value;
  axios.defaults.xsrfCookieName = "csrftoken";
  axios.defaults.xsrfHeaderName = "X-CSRFToken";
  if (email == "") {
    alert("이메일을 입력하세요!");
    return false;
  }
  if (!emailForm.test(email)) {
    alert("이메일 형식을 지켜주세요!");
    email1.focus();
    return false;
  }
  axios
    .post("/logins/signup/emailCheck", {
      email: email,
    })
    .then((response) => {
      if (response.data.result == "fail") {
        alert("해당 이메일는 이미 존재하는 이메일입니다.");
        return false;
      } else {
        alert("사용 가능한 이메일입니다.");
        document.querySelector("#id_email").value =
          document.querySelector("#id_email1").value;
        document.querySelector("#error_email").innerHTML = "";
        return true;
      }
    });
});
