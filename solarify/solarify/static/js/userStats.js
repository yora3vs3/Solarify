const getHumanMonth = (m) => {
  const [_, month, __] = new Date(new Date().getFullYear(), m - 1, 1)
    .toDateString()
    .split(" ");
  return month;
};

const updateTopMonthsUI = (topMonth, type) => {
  if (type === "usage") {
    document.querySelector(".usage-top-month").textContent = getHumanMonth(
      Object.keys(topMonth)[0]
    );
    document.querySelector(
      ".usage-top-month-value"
    ).textContent = Object.values(topMonth)[0];
  } else {
    document.querySelector(".production-top-month").textContent = getHumanMonth(
      Object.keys(topMonth)[0]
    );
    document.querySelector(
      ".production-top-month-value"
    ).textContent = Object.values(topMonth)[0];
  }
};

const updateThisMonthUI = (data = [], type = "usage") => {
  const currentMonthNumber = new Date().getMonth() + 1;

  const currentMonthData = data.find((item, i) => {
    const key = currentMonthNumber;
    // TODO
    return item;
  });

  if (type === "usage") {
    document.querySelector(".usage-this-month").textContent = getHumanMonth(
      Object.keys(currentMonthData)[0]
    );
    document.querySelector(
      ".usage-this-month-value"
    ).textContent = Object.values(currentMonthData)[0];
  } else {
    document.querySelector(".production-this-month").textContent = getHumanMonth(
      Object.keys(currentMonthData)[0]
    );
    document.querySelector(
      ".production-this-month-value"
    ).textContent = Object.values(currentMonthData)[0];
  }
};

const formatStats = (data = {}, type = "usage") => {
  const monthData = data.months;
  console.log("monthData", monthData);
  const vals = Object.values(monthData);
  const s = vals.map((item, i) => ({ [i + 1]: item }));

  const sorted = s.sort((a, b) =>
    Object.values(a)[0] > Object.values(b)[0] ? -1 : 1
  );
  const topMonth = sorted[0];
  if (type === "usage") {
    updateThisMonthUI(s, "usage");
  }
  if (type === "production") {
    updateThisMonthUI(s, "production");
  }

  updateTopMonthsUI(topMonth, type);
};

const setGraphs = (data) => {};
const fetchData = () => {
  const promise1 = fetch("/usage_summary_rest")
    .then((res) => res.json())
    .then((data) => Promise.resolve(data))
    .catch((e) => Promise.reject(e));
  const promise2 = fetch("/last_3months_stats")
    .then((res) => res.json())
    .then((data) => Promise.resolve(data))
    .catch((e) => Promise.reject(e));
  const promise3 = fetch("/production/production_sources_data")
    .then((res) => res.json())
    .then((data) => Promise.resolve(data))
    .catch((e) => Promise.reject(e));
  const promise4 = fetch("/production/production_summary_rest")
    .then((res) => res.json())
    .then((data) => Promise.resolve(data))
    .catch((e) => Promise.reject(e));

  Promise.all([promise1, promise2, promise3, promise4])
    .then((data) => {
      const [
        thisYearusage,
        usageCategories,
        productionSources,
        thisYearproduction,
      ] = data;
      formatStats(thisYearusage.this_year_usage_data, "usage");
      formatStats(thisYearproduction.this_year_production_data, "production");
      setGraphs(data);
    })
    .catch((errs) => console.log("errs", errs));
};

window.onload = () => fetchData();
