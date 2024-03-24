        # TESSDATA_PREFIX='C:\Program Files\Tesseract-OCR'

        # custom_config = r'--oem 3 --psm 6'

        # lice=pytesseract.image_to_string(PIL.Image.open(license),config=custom_config)

        # print(''.join(lice))
        # return redirect('home_user_reg')


        # image = cv2.imread('media/images.jpeg')
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray, (3,3), 0)
        # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # # Morph open to remove noise and invert image
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        # invert = 255 - opening

        # # Perform text extraction
        # data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
        # print(data,'asdasdasasd222')




        # image = cv2.imread('media/data_set/images (7).jpeg')
        # image = imutils.resize(image, width=300 )
        # cv2.imshow("original image", image)
        # cv2.waitKey(0)

        # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("greyed image", gray_image)
        # cv2.waitKey(0)

        # gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17) 
        # cv2.imshow("smoothened image", gray_image)
        # cv2.waitKey(0)

        # edged = cv2.Canny(gray_image, 30, 200) 
        # cv2.imshow("edged image", edged)
        # cv2.waitKey(0)

        # cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # image1=image.copy()
        # cv2.drawContours(image1,cnts,-1,(0,255,0),3)
        # cv2.imshow("contours",image1)
        # cv2.waitKey(0)

        # cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
        # screenCnt = None
        # image2 = image.copy()
        # cv2.drawContours(image2,cnts,-1,(0,255,0),3)
        # cv2.imshow("Top 30 contours",image2)
        # cv2.waitKey(0)

        # i=7
        # for c in cnts:
        #     perimeter = cv2.arcLength(c, True)
        #     approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        #     if len(approx) == 4: 
        #             screenCnt = approx

        
        #             x,y,w,h = cv2.boundingRect(c) 
        #             new_img=image[y:y+h,x:x+w]
        #             cv2.imwrite('./'+str(i)+'.png',new_img)
        #             i+=1
        #             break


        # cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
        # cv2.imshow("image with detected license plate", image)
        # cv2.waitKey(0)


        # Cropped_loc = './7.png'
        # cv2.imshow("cropped", cv2.imread(Cropped_loc))
        # plate = pytesseract.image_to_string(Cropped_loc, lang ='eng')
        # license_no = "".join(plate.split()).replace(":", "").replace("-", "").replace("~", "")        
        # print("Number plate is:", license_no)
        # # pn=(''.join(plate.split()))
        # # print(pn,'without spaces')
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


                        #interaction=InteractionModel.objects.create(message= message,interac_type = 'email',from_user=user_id,to_user=driver_id)
