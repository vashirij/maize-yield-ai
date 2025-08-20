<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />

    <title>Maize Yield Prediction</title>

    <link rel="stylesheet" href="style.css" />

    <!-- Bootstrap CSS CDN -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css"
        integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous" />

    <!-- Font Awesome JS -->
    <script src="https://kit.fontawesome.com/728d1d3dec.js" crossorigin="anonymous"></script>

    <!-- jQuery CDN -->
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <!-- Popper.JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"
        integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous">
    </script>
    <!-- Bootstrap JS -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"
        integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous">
    </script>
</head>

<body>
    <div class="svgs">
        <img src="imgs/bg_svg.svg" alt="Background SVG" />
    </div>

    <div class="page" id="part1">
        <div class="info">
            <div class="heading">
                <div class="title text-primary">Machine Learning Model for</div>
                <div class="title text-primary">Maize Yield Prediction in</div>
                <div class="title text-primary">Marondera, Zimbabwe</div>
                <br /><br />
            </div>
            <div class="title text-primary">BSEH 480 IT Capstone Project 2</div>
            <div class="title text-primary">James Vashiri (P1863122E)</div>
            <br /><br />
            <div class="btn-grp">
                <a href="#part3" class="try btn btn-outline-primary">Try it!</a>
            </div>
        </div>
        <div class="imgContainer">
            <img src="imgs/flowers.svg" alt="Flowers Illustration" />
        </div>
    </div>

    <div class="container p-5 page" id="part3">
        <div class="card shadow-lg col-12 col-md-8 col-lg-6 mx-auto p-0">
            <div class="card-header text-primary text-center">
                <h3><u>Maize Yield Prediction</u></h3>
            </div>
            <div class="card-body">
                <div class="form-group">
                    <label for="district">District:</label>
                    <select class="form-control" name="district" id="district" aria-required="true"></select>
                </div>
                <div class="form-group">
                    <label for="crop">Crop:</label>
                    <select class="form-control" name="crop" id="crop" aria-required="true"></select>
                </div>
                <div class="form-group">
                    <label for="area">Area (in hectares):</label>
                    <input type="number" step="any" min="100" max="10000000" class="form-control" id="area"
                        placeholder="Enter area in hectares" aria-required="true" />
                    <small id="areaHelp" class="form-text text-muted">Enter a value between 1 and 10,000,000</small>
                </div>
                <div class="form-group">
                    <label for="soil">Soil:</label>
                    <select class="form-control" name="soil" id="soil" aria-required="true"></select>
                </div>
                <div class="text-center">
                    <button class="btn btn-primary" id="submit" disabled>Predict</button>
                </div>
            </div>
            <div class="card-footer" id="prediction" style="display: none;"></div>
        </div>
    </div>

    <script>
        $(document).ready(() => {
            const $submitBtn = $('#submit');
            const $prediction = $('#prediction');

            $submitBtn.prop('disabled', true);
            $prediction.hide();

            let input_lists;

            // Load input lists from JSON file
            $.get('input_lists.txt', (data) => {
                input_lists = JSON.parse(data);

                let opts = '<option value="" selected hidden disabled>Select district</option>';
                input_lists['districts'].forEach(d => {
                    opts += `<option value="${d}">${d}</option>`;
                });
                $('#district').html(opts);

                opts = '<option value="" selected hidden disabled>Select crop</option>';
                input_lists['crops'].forEach(c => {
                    opts += `<option value="${c}">${c}</option>`;
                });
                $('#crop').html(opts);

                opts = '<option value="" selected hidden disabled>Select soil type</option>';
                input_lists['soils'].forEach(s => {
                    opts += `<option value="${s}">${s}</option>`;
                });
                $('#soil').html(opts);
            });

            // Form validation function
            function validateForm() {
                const district = $('#district').val();
                const crop = $('#crop').val();
                const soil = $('#soil').val();
                const area = $('#area').val();

                const areaNum = parseFloat(area);
                const isAreaValid = areaNum >= 100 && areaNum <= 10000000;

                const isValid = district && crop && soil && isAreaValid;
                $submitBtn.prop('disabled', !isValid);
            }

            // Trigger validation on input change
            $('select, #area').on('change keyup', validateForm);

            // Submit button click handler
            $submitBtn.on('click', () => {
                const areaVal = $('#area').val().trim();
                const areaNum = parseFloat(areaVal);

                if (isNaN(areaNum) || areaNum < 100 || areaNum > 10000000) {
                    alert("Please enter a valid numeric value for Area between 100 and 10,000,000.");
                    return;
                }

                const params = $.param({
                    district: $('#district').val(),
                    crop: $('#crop').val(),
                    area: areaVal,
                    soil: $('#soil').val(),
                });

                // Show loading text
                $prediction.html('<div class="text-center text-info"><i class="fas fa-spinner fa-spin"></i> Predicting...</div>');
                $prediction.show();

                $.get('predict.php?' + params, (data) => {
                    $prediction.html(data);
                }).fail(() => {
                    $prediction.html('<div class="text-danger text-center">An error occurred while fetching the prediction. Please try again.</div>');
                });
            });
        });
    </script>
</body>

</html>
