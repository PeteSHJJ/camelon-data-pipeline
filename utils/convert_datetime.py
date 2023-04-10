import datetime 

def split_thai_datetime_thairath(text):
    months_th = {
        "ม.ค.": 1,
        "ก.พ.": 2,
        "มี.ค.": 3,
        "เม.ย.": 4,
        "พ.ค.": 5,
        "มิ.ย.": 6,
        "ก.ค.": 7,
        "ส.ค.": 8,
        "ก.ย.": 9,
        "ต.ค.": 10,
        "พ.ย.": 11,
        "ธ.ค.": 12
    }
    
    date_parts = text.split()  # split the text into a list of words
    day = int(date_parts[0])  # extract the day as an integer
    month = months_th[date_parts[1]]    # extract the month abbreviation as a string
    year = int(date_parts[2]) - 543 # extract the year as an integer
    time_parts = date_parts[3].split(":") 
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    
    dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def split_thai_datetime_dailynews(text):

    months_th = {
        "มกราคม": 1,
        "กุมภาพันธ์": 2,
        "มีนาคม": 3,
        "เมษายน": 4,
        "พฤษภาคม": 5,
        "มิถุนายน": 6,
        "กรกฎาคม": 7,
        "สิงหาคม": 8,
        "กันยายน": 9,
        "ตุลาคม": 10,
        "พฤศจิกายน": 11,
        "ธันวาคม": 12
    }
    
    
    date_parts = text.split()  # split the text into a list of words
    day = int(date_parts[1])  # extract the day as an integer
    month = months_th[date_parts[2]]    # extract the month abbreviation as a string
    year = int(date_parts[3]) - 543 # extract the year as an integer
    time_parts = date_parts[5].split(".") 
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    
    dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    return dt.strftime("%Y-%m-%d %H:%M:%S")