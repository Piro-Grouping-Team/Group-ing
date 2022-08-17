let startDate, endDate; // 시작 날짜, 끝 날짜 저장
let date;

const getDates = async (meetId) => {
  const url = "/calendar/getDates/"; // 요청 URL
  const { data } = await axios.post(url, { meetId }); // 요청 결과 받기
  handleDates(data, meetId); // 시작 날짜, 끝 날짜 저장
  return;
}; // 시작 끝 날짜 가져오기

const handleDates = async (data, meetId) => {
  startDate = new Date(data.startDate); // 시작 날짜 저장
  endDate = new Date(data.endDate); // 끝 날짜 저장
  date = startDate;
  sMonth = startDate.getMonth();
  eMonth = endDate.getMonth();

  sDate = startDate.getDate();
  eDate = endDate.getDate();

  validList = [];
  for (let i = sMonth; i < eMonth + 1; i++) {
    validList.push(i);
  }

  makeCalendar(meetId, data.meetType);
  return;
};

const makeCalendar = async (meetId, meetType) => {
  const viewYear = date.getFullYear(); //2022
  const viewMonth = date.getMonth(); // 6 / 0 1 2 3...

  // 캘린더 년도 달 채우기
  //   locale = "en-us";
  //   const month = date.toLocaleString(locale, { month: "long" });

  document.querySelector(".year-month").textContent = `
   ${viewYear} ${viewMonth + 1} 
  `;

  // 이번 달 마지막 날짜 가져오기
  const thisLast = new Date(viewYear, viewMonth + 1, 0);
  // 일에 0을 넣으면 마지막 날짜가 가져와진다!
  const thisDate = thisLast.getDate();
  const thisDay = thisLast.getDay();

  // 저번 달 마지막 날짜 가져오기
  const prevLast = new Date(viewYear, viewMonth, 0);
  const prevDate = prevLast.getDate();
  const prevDay = prevLast.getDay();

  // 전체 날짜를 만들기 위한 배열 만들기
  const prevDates = [];
  const thisDates = [...Array(thisDate + 1).keys()].slice(1);
  // Array(32) 길이가 32인 배열 [undefined, undefined, ... , undefined]
  // .keys() [0, 1, 2, ... , 31]
  // .slice(1) >> 첫번째 인덱스 날림
  const nextDates = [];

  // 저번달의 마지막 날이 토요일이면 저번달 달력 표시 안해도 됨
  // 이전 달 날짜들을 만들어주는 코드
  if (prevDay !== 6) {
    for (let i = 0; i < prevDay + 1; i++) {
      prevDates.unshift(prevDate - i);
    }
  }

  // thisDay는 마지막 날짜의 요일!
  // 다음 달 날짜들을 만들어주는 코드
  for (let i = 1; i < 7 - thisDay; i++) {
    nextDates.push(i);
  }

  const firstDateIndex =
    viewMonth == sMonth ? thisDates.indexOf(sDate) : thisDates.indexOf(1);
  // 시작달이면 시작날짜부터, 시작달이 아니면 처음부터

  const lastDateIndex =
    viewMonth == eMonth
      ? thisDates.indexOf(eDate)
      : thisDates.lastIndexOf(thisDate);
  // 마지막달이면 끝날짜까지, 마지막달이 아니면 끝까지

  const allUsers = 10;

  // 달에 대한 정보를 받아와서 날짜로 접근해서 정보를 가져오기
  // 렌더링 시 -> ajax 하나
  // 클릭시 -> ajax로 사람들 정보 가져오기
  if (meetType === "today") {
    const url = "/calendar/getDayInfo/";
    const { data } = await axios.post(url, { viewYear, viewMonth, meetId });
    // 범위에 해당X other 범위 해당 this
    thisDates.forEach((date, i) => {
      if (i >= firstDateIndex && i < lastDateIndex + 1) {
        const maxCount = () => {
          let max = 0;
          for (let j = 0; j < data.dayInfo.length; j++) {
            if (date == data.dayInfo[j].day) {
              if (max < data.dayInfo[j].userCount) {
                max = data.dayInfo[j].userCount;
              }
            }
          }
          return max;
        };
        console.log(maxCount());

        //색깔 판별로직
        thisDates[i] = `
    <div class = "date"><div class="this date-content" style="background: rgba(198, 252, 35, ${
      maxCount() / allUsers
    })"><span>${date}</span></div></div>
    `;
      } else {
        thisDates[i] = `
        <div class = "date"><div class = "other date-content"><span class ="other">${date}</span></div></div>
        `;
      }
    });
  } else {
    //여행 정보 불러오기
    const url = "/calendar/getTravelInfo/";
    const { data } = await axios.post(url, { viewYear, viewMonth, meetId });

    // 범위에 해당X other 범위 해당 this
    thisDates.forEach((date, i) => {
      if (i >= firstDateIndex && i < lastDateIndex + 1) {
        let userCount = 0;
        for (let j = 0; j < data.travelInfo.length; j++) {
          if (date == data.travelInfo[j].day) {
            userCount = data.travelInfo[j].userCount;
          }
        }
        console.log(userCount);
        //색깔 판별로직
        thisDates[i] = `
        <div class = "date"><div class = "this date-content" style="background:rgba(198,252,35,${
          userCount / allUsers
        }"><span>${date}</span></div></div>
        `;
      } else {
        thisDates[i] = `
        <div class = "date"><div class = "other date-content"><span class ="other">${date}</span></div></div>
        `;
      }
    });
  }

  prevDates.forEach((date, i) => {
    prevDates[i] = `
    <div class = "date"></div>
    `;
  });

  nextDates.forEach((date, i) => {
    nextDates[i] = `
    <div class = "date"></div>
    `;
  });

  const dates = prevDates.concat(thisDates, nextDates);

  // Dates 그리기
  document.querySelector(".dates").innerHTML = dates.join("");
};

// 이전 달로 이동
const prevMonth = () => {
  if (validList.includes(date.getMonth() - 1)) {
    date.setMonth(date.getMonth() - 1); // 전 달로 달 변경
    date.setDate(1); // 전 달로 날짜 변경
    makeCalendar();
  }
};

// 다음 달로 이동
const nextMonth = () => {
  if (validList.includes(date.getMonth() + 1)) {
    date.setDate(1); // 다음 달로 날짜 변경
    date.setMonth(date.getMonth() + 1); // 다음 달로 달 변경
    makeCalendar();
  }
};

const selectDate = document.querySelectorAll(".this");

console.log(selectDate);

const myClick = () => {
  console.log("hi!");
};

for (i = 0; i < selectDate.length; i++) {
  selectDate[i].addEventListener("click", myClick);
  // selectDate[i].removeEventListener("click", myClick);
}
