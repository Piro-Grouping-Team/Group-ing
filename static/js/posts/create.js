const addBtn1 = document.querySelector(".place-add");
const places = document.querySelector(".places");
addBtn1.addEventListener("click", () => {
  let place = document.createElement("input");
  place.setAttribute("class", "log-input");
  place.setAttribute("type", "text");
  place.setAttribute("placeholder", "장소를 추가해주세요");
  place.setAttribute("name", "place[]");
  places.appendChild(place);
});

const addBtn2 = document.querySelector(".img-add");
const images = document.querySelector(".images");
addBtn2.addEventListener("click", () => {
  let image = document.createElement("input");
  image.setAttribute("type", "file");
  image.setAttribute("name", "logImgs[]");
  images.appendChild(image);
});

const loadMeetingInfo = async (value) => {
  axios.defaults.xsrfCookieName = "csrftoken";
  axios.defaults.xsrfHeaderName = "X-CSRFToken";
  const element = document.querySelector('#meetingsMembers')
  const meetPlaceElement = document.querySelector('#meetPlace')

  const startTimeInputElement = document.querySelector('#startTimeI')
  const endTimeInputElement = document.querySelector('#endTimeI')
  const startTimeParagraphElement = document.querySelector('#startTimeP')
  const endTimeParagraphElement = document.querySelector('#endTimeP')

  const {data} = await axios.post(
    '/posts/loadMeetingMembers',
    {
      'meetingId': value,
    },);
  for (i = 0; i < data.members.length; i++){
    element.innerHTML = `<div class="user-name">${data.members[i]}</div>`
  }
  console.log(typeof(data.startTime))
  meetPlaceElement.value = data.place;
  startTimeInputElement.value = data.startTime;
  endTimeInputElement.value = data.endTime;
  startTimeParagraphElement.innerText = data.startTime;
  endTimeParagraphElement.innerText = data.endTime;
}



const logForm = () => {
  const meetId = document.getElementById('meetId').value;
  const logTitle = document.getElementById('logTitle').value;
  const meetPlace = document.getElementById('meetPlace').value;
  const logContent = document.getElementById('logContent').value;

  if (meetId == ''){
    alert('약속을 정해주세요!');
    meetId.focus();
    return false;
  }

  if (logTitle == ''){
    alert('제목을 정해주세요!');
    logTitle.focus();
    return false;
  }

  if (meetPlace == ''){
    alert('약속장소를 정해주세요!');
    meetPlace.focus();
    return false;
  }

  if (logContent == ''){
    alert('본문내용을 작성해주세요!');
    logContent.focus();
    return false;
  }
  
  document.createPost.submit();
}