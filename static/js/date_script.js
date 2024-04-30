const currentDate = document.querySelector(".current-date");
const daysTag = document.querySelector(".days");
const prevNextIcon = document.querySelectorAll(".icons span");

let date = new Date(),
    currYear = date.getFullYear(),
    currMonth = date.getMonth();

const months = ["Январь", "Февраль", "Март",
                "Апрель", "Май", "Июнь",
                "Июль", "Август", "Сентябрь",
                "Октябрь", "Ноябрь", "Декабрь"]
;

const renderCalendar = () => {
    let firstDayofMonth = new Date(currYear, currMonth, 1).getDay();
    let lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate();
    let lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay();
    let lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate();
    let liTag = "";

    for (let i = firstDayofMonth; i > 0; i--) {
        liTag += `<li class="inactive" onclick="prevMonth()">${lastDateofLastMonth - i + 1}</li>`;
    }
    
    for (let i = 1; i <= lastDateofMonth; i++) {
        let isToday = i === date.getDate() && currMonth === new Date().getMonth() && currYear === new Date().getFullYear() ? "active" : "";
        liTag += `<li class="${isToday}" onclick="selectDay(this)">${i}</li>`;
    }
    
    for (let i = lastDayofMonth; i < 6; i++) {
        liTag += `<li class="inactive" onclick="nextMonth()">${i - lastDayofMonth + 1}</li>`;
    }
    
    currentDate.innerText = `${months[currMonth]} ${currYear}`
    daysTag.innerHTML = liTag;
}
renderCalendar();

function prevMonth() {
    currMonth = currMonth === 0 ? 11 : currMonth - 1;
    currYear = currMonth === 11 ? currYear - 1 : currYear;
    updateCalendar();
}

function nextMonth() {
    currMonth = currMonth === 11 ? 0 : currMonth + 1;
    currYear = currMonth === 0 ? currYear + 1 : currYear;
    updateCalendar();
}




prevNextIcon.forEach(icon => {
    icon.addEventListener("click", () => {
        if (icon.id === "prev") {
            currMonth = currMonth === 0 ? 11 : currMonth - 1;
            currYear = currMonth === 11 ? currYear - 1 : currYear;
        } else {
            currMonth = currMonth === 11 ? 0 : currMonth + 1;
            currYear = currMonth === 0 ? currYear + 1 : currYear;
        }
        renderCalendar();
    })
});
let selectedStartDate = null;
let selectedEndDate = null;

function selectDay(element) {
    const selectedDay = document.querySelector('.days li.active');
    if (selectedDay) {
        selectedDay.classList.remove('active');
    }
    element.classList.add('active');

    const selectedDate = new Date(currYear, currMonth, parseInt(element.innerText));
    selectedDate.setDate(selectedDate.getDate() + 1); // Добавляем 1 день

    if (!selectedStartDate || (selectedStartDate && selectedEndDate)) {
        // If no start date is selected or both start and end dates are selected, set new start date
        selectedStartDate = selectedDate;
        selectedEndDate = null;
    } else if (selectedStartDate && !selectedEndDate) {
        // If start date is selected but end date is not selected, set end date
        if (selectedDate > selectedStartDate) {
            selectedEndDate = selectedDate;
        } else {
            selectedEndDate = selectedStartDate;
            selectedStartDate = selectedDate;
        }
        document.getElementById('start_date').value = selectedStartDate.toISOString().split('T')[0];
        document.getElementById('end_date').value = selectedEndDate.toISOString().split('T')[0];
        console.log("Start Date:", selectedStartDate.toISOString().split('T')[0]);
        console.log("End Date:", selectedEndDate.toISOString().split('T')[0]);
    }

    if (selectedStartDate && selectedEndDate) {
        // Highlight the range between selected start and end dates
        highlightDateRange(selectedStartDate, selectedEndDate);
    }
}


function highlightDateRange(startDate, endDate) {
    const days = document.querySelectorAll('.days li');
    days.forEach(day => {
        const dayDate = new Date(currYear, currMonth, parseInt(day.innerText)+1);
        if (dayDate >= startDate && dayDate <= endDate) {
            day.classList.add('selected-range');
        } else {
            day.classList.remove('selected-range');
        }
    });
}

function updateCalendar() {
    renderCalendar();
    selectedStartDate = null;
    selectedEndDate = null;
}
