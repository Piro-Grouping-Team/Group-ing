class Time {
  constructor(year, month, day, hour, pnum) {
    this.year = year;
    this.month = month;
    this.day = day;
    this.hour = hour;
    this.pnum = pnum;
  }
}

const sTime = new Time(2022, 8, 18, 15, 0);
const eTime = new Time(2022, 8, 20, 12, 0);

const times = [];

for (i = sTime.hour; i < 24; i++) {
  num = sTime.pnum + 1;
  times.push(new Time(2022, 8, 18, i, num));
}
// 시작 날짜의 시간들 배열에 넣기

for (y = sTime.year; y < eTime.year + 1; y++) {
  for (i = sTime.month; i < eTime.month + 1; i++) {
    for (j = sTime.day + 1; j < eTime.day; j++) {
      for (k = 0; k < 24; k++) {
        num = sTime.pnum + 1;
        times.push(new Time(y, i, j, k, num));
      }
    }
  }
}
// 중간 24시간 다 되는 시간들 배열에 넣기

for (i = 0; i <= eTime.hour; i++) {
  num = sTime.pnum + 1;
  times.push(new Time(2022, 8, 20, i, num));
}
// 마지막 날짜의 시간들 배열에 넣기

const hours = [];

const dayTimes = times.filter(
  (i) => i.year == 2022 && i.month == 8 && i.day == 20 && i.pnum == 1
);

console.log(dayTimes);

for (i = 0; i < 24; i++) {
  let condition = "";
  if (dayTimes.find((index) => index.hour === i)) {
    condition = `rgba(255,0,0,${(1 / 7) * 1})`;
  }
  hours[i] = `
       <div style = "color:${condition}">${i}</div>
       `;
}

document.querySelector(".times").innerHTML = hours.join("");
