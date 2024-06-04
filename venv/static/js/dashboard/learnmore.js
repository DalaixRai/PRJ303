document.addEventListener("DOMContentLoaded", function () {
  const learnMoreLinks = document.querySelectorAll(".learn-more-link");
  const showLessLinks = document.querySelectorAll(".show-less-link");
  const expandableContents = document.querySelectorAll(".expandable-content");
  const summaryTexts = document.querySelectorAll(".summary-text");

  // Loop through each pair of elements
  learnMoreLinks.forEach((learnMoreLink, index) => {
    const showLessLink = showLessLinks[index];
    const expandableContent = expandableContents[index];
    const summaryText = summaryTexts[index];

    if (learnMoreLink && showLessLink && expandableContent && summaryText) {
      // Set initial state: hide expandable content, show summary text
      expandableContent.style.display = "none";
      summaryText.style.display = "block";
      learnMoreLink.style.display = "inline";
      showLessLink.style.display = "none";

      // Attach click event listener to "Learn more" link
      learnMoreLink.addEventListener("click", function (event) {
        event.preventDefault();
        expandableContent.style.display = "block";
        summaryText.style.display = "none";
        learnMoreLink.style.display = "none";
        showLessLink.style.display = "inline";
      });

      // Attach click event listener to "Show less" link
      showLessLink.addEventListener("click", function (event) {
        event.preventDefault();
        expandableContent.style.display = "none";
        summaryText.style.display = "block";
        learnMoreLink.style.display = "inline";
        showLessLink.style.display = "none";
      });
    }
  });
});



