document.addEventListener("DOMContentLoaded", () => {

    const birthdayStr = USER_BIRTHDAY;  
    const birthday = new Date(birthdayStr);

    const deadlineInput = document.getElementById("limit_age");
    const ageDisplay = document.getElementById("age-display");   // 年齢表示
    const errorMsg = document.getElementById("deadline-error");

    // 初期表示(年齢のみリセット)
    function resetAgeDisplay() {
        ageDisplay.textContent = "ー歳";
    }

    // 完全な初期化(エラーも含む)
    function setInitialDisplay() {
        resetAgeDisplay();
        errorMsg.textContent = "";
    }

    setInitialDisplay();

    const updateAge = () => {
        const deadlineStr = deadlineInput.value;
        console.log("入力値:", deadlineStr);
        // 入力なし
        if (!deadlineStr) {
            setInitialDisplay();
            return;
        }

        const deadline = new Date(deadlineStr);
        deadline.setHours(0,0,0,0); 
        const futureYear = deadline.getFullYear();

        const birthYear = birthday.getFullYear();
        const birthMonth = birthday.getMonth();
        const birthDay = birthday.getDate();

        let age = futureYear - birthYear;

        const hasBirthdayPassed =
            (deadline.getMonth() > birthMonth) ||
            (deadline.getMonth() === birthMonth && deadline.getDate() >= birthDay);

        if (!hasBirthdayPassed) {
            age -= 1;
        }

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        // 過去日チェック
        if (deadline < today) {
            errorMsg.textContent = "※ 過去の日付は設定できません。";
            resetAgeDisplay();
            return;
        } else {
            errorMsg.textContent = "";
        }

        // 年と歳を表示
        ageDisplay.textContent = `${futureYear}年：${age}歳`;
    };

    // input の変更時にリアルタイム更新
    deadlineInput.addEventListener("input", updateAge);
    deadlineInput.addEventListener("change", updateAge);

    // 初期値があればロード時に反映
    if (deadlineInput.value) {
        updateAge();
    }
});
