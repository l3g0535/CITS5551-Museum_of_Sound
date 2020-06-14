from mixer.backend.django import mixer

class TestModels:

    def test_Production_storagelocation(models.Model):
        product = mixer.blend('frontend.Production', storage_location ='productions')
        assert product.storage_location == 'productions'

    def test_Production_ID(models.Model):
        product = mixer.blend('frontend.Production', prod_id = 1)
        assert product.prod_id == 1

    def test_Production_Title(models.Model):
        product = mixer.blend('frontend.Production',prod_title = 'test1')
        assert product.prod_title == 'test1'
        
    def test_Production_Title(models.Model):
        product = mixer.blend('frontend.Production',prod_title = '')
        assert product.prod_title == ''

    def test_Production_UploadTime(models.Model):
        product = mixer.blend('frontend.Production',DateTimeField = '09/05/19T06:53:32')
        assert product.upload_time == '09/05/19T06:53:32'

    def test_Production_Description(models.Model):
        product = mixer.blend('frontend.Production',prod_description = 'test2')
        assert product.prod_description == 'test2'
        
    def test_Production_Description(models.Model):
        product = mixer.blend('frontend.Production',prod_description = '')
        assert product.prod_description == ''

    def test_Production_IsApproved(models.Model):
        product = mixer.blend('frontend.Production',is_approved = 'Yes')
        assert product.is_approved == 'Yes'
        
    def test_Production_image(models.Model):
        product = mixer.blend('frontend.Production', image = 'test1.png')
        assert product.image == 'test1.png'
        
    def test_Production_image(models.Model):
        product = mixer.blend('frontend.Production', image = 'test1.jpg')
        assert product.image == 'test1.jpg'
        
    def test_Production_image(models.Model):
        product = mixer.blend('frontend.Production', image = 'test1.mp3')
        assert product.image == 'test1.mp3'
        
    def test_Production_image(models.Model):
        product = mixer.blend('frontend.Production', image = 'test1.wav')
        assert product.image == 'test1.wav'
        
    def test_Production_image(models.Model):
        product = mixer.blend('frontend.Production', image = '')
        assert product.image == ''
        
    def test_Production_audifile(models.Model):
        product = mixer.blend('frontend.Production', audio_file = 'test1.png')
        assert product.audio_file == 'test1.png'
        
    def test_Production_audifile(models.Model):
        product = mixer.blend('frontend.Production', audio_file = 'test1.jpg')
        assert product.audio_file == 'test1.jpg'
        
    def test_Production_audifile(models.Model):
        product = mixer.blend('frontend.Production', audio_file = 'test1.mp3')
        assert product.audio_file == 'test1.mp3'
        
    def test_Production_audifile(models.Model):
        product = mixer.blend('frontend.Production', audio_file = 'test1.wav')
        assert product.audio_file == 'test1.wav'
        
    def test_Production_audifile(models.Model):
        product = mixer.blend('frontend.Production', audio_file = '')
        assert product.audio_file == ''

    
    
    
    def test_UserSound_storagelocation(models.Model):
        product = mixer.blend('frontend.UserSound', storage_location='productions')
        assert product.storage_location == 'productions'
    

    def test_UserSound_ID(models.Model):
        product = mixer.blend('frontend.UserSound', prod_id=1)
        assert product.prod_id == 1


    def test_UserSound_Title(models.Model):
        product = mixer.blend('frontend.UserSound', prod_title='test1')
        assert product.prod_title == 'test1'
        
        
    def test_UserSound_Title(models.Model):
        product = mixer.blend('frontend.UserSound', prod_title='')
        assert product.prod_title == ''


    def test_UserSound_UploadTime(models.Model):
        product = mixer.blend('frontend.UserSound', DateTimeField='09/05/19T06:53:32')
        assert product.upload_time == '09/05/19T06:53:32'


    def test_UserSound_Description(models.Model):
        product = mixer.blend('frontend.UserSound', prod_description='test2')
        assert product.prod_description == 'test2'
        
        
    def test_UserSound_Description(models.Model):
        product = mixer.blend('frontend.UserSound', prod_description='')
        assert product.prod_description == ''


    def test_UserSound_IsApproved(models.Model):
        product = mixer.blend('frontend.UserSound', is_approved='Yes')
        assert product.is_approved == 'Yes'
        
    
    def test_UserSound_image(models.Model):
        product = mixer.blend('frontend.UserSound', image = 'test1.png')
        assert product.image == 'test1.png'
        
    def test_UserSound_image(models.Model):
        product = mixer.blend('frontend.UserSound', image = 'test1.jpg')
        assert product.image == 'test1.jpg'
        
    def test_UserSound_image(models.Model):
        product = mixer.blend('frontend.UserSound', image = 'test1.mp3')
        assert product.image == 'test1.mp3'
        
    def test_UserSound_image(models.Model):
        product = mixer.blend('frontend.UserSound', image = 'test1.wav')
        assert product.image == 'test1.wav'
        
    def test_UserSound_image(models.Model):
        product = mixer.blend('frontend.UserSound', image = '')
        assert product.image == ''
        
    def test_UserSound_audifile(models.Model):
        product = mixer.blend('frontend.UserSound', audio_file = 'test1.png')
        assert product.audio_file == 'test1.png'
        
    def test_UserSound_audifile(models.Model):
        product = mixer.blend('frontend.UserSound', audio_file = 'test1.jpg')
        assert product.audio_file == 'test1.jpg'
        
    def test_UserSound_audifile(models.Model):
        product = mixer.blend('frontend.UserSound', audio_file = 'test1.mp3')
        assert product.audio_file == 'test1.mp3'
        
    def test_UserSound_audifile(models.Model):
        product = mixer.blend('frontend.UserSound', audio_file = 'test1.wav')
        assert product.audio_file == 'test1.wav'
        
    def test_UserSound_audifile(models.Model):
        product = mixer.blend('frontend.UserSound', audio_file = '')
        assert product.audio_file == ''
